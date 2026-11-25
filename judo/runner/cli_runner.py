"""
Thin, dependency-free test execution used by ``judo run`` and the MCP server.

Runs behave in subprocesses (isolated, CI friendly, honest exit codes).
Parallel mode runs one subprocess per feature file.
"""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, List, Optional

JSON_FORMATTER = "judo.behave.json_formatter:JudoJsonFormatter"
RERUN_FILE = "rerun_failing.features"


def _feature_files(paths: List[str], cwd: Path) -> List[Path]:
    files: List[Path] = []
    for p in paths:
        path = (cwd / p) if not os.path.isabs(p) else Path(p)
        if path.is_dir():
            files.extend(sorted(path.rglob("*.feature")))
        elif path.suffix == ".feature":
            files.append(path)
    return files


def _base_cmd(tags: Optional[List[str]], fail_fast: bool, dry_run: bool) -> List[str]:
    cmd = [sys.executable, "-m", "behave", "--no-skipped"]
    for t in tags or []:
        cmd += ["--tags", t.lstrip("@") if not t.startswith("~") else t]
    if fail_fast:
        cmd.append("--stop")
    if dry_run:
        cmd.append("--dry-run")
    return cmd


def _find_project_root(paths: List[str], cwd: Path) -> Path:
    """behave needs to run from the folder that contains ``features/``."""
    first = Path(paths[0]) if paths else Path(".")
    start = first if first.is_absolute() else (cwd / first)
    start = start if start.is_dir() else start.parent
    for parent in [start.resolve()] + list(start.resolve().parents):
        if (parent / "features" / "environment.py").exists():
            return parent
        if parent.name == "features" and (parent / "environment.py").exists():
            return parent.parent
    return cwd


def run_tests(paths: Optional[List[str]] = None, tags: Optional[List[str]] = None,
              env: Optional[str] = None, parallel: bool = False, workers: int = 4,
              fail_fast: bool = False, rerun_failed: bool = False, fmt: str = "pretty",
              dry_run: bool = False, cwd: Optional[str] = None, verbose: bool = False,
              timeout: Optional[int] = None, stream: bool = False, junit: bool = False,
              retries: int = 0) -> Dict:
    """Run feature files and return ``{returncode, passed, summary, result_file, output}``."""
    cwd_p = Path(cwd or os.getcwd()).resolve()
    paths = paths or ["features"]
    root = _find_project_root(paths, cwd_p)
    out_dir = root / "judo_reports"
    out_dir.mkdir(exist_ok=True)
    result_file = out_dir / "result.json"

    child_env = dict(os.environ)
    if env:
        child_env["KARATE_ENV"] = env
        child_env["JUDO_ENV"] = env
    child_env.setdefault("PYTHONIOENCODING", "utf-8")

    cmd_base = _base_cmd(tags, fail_fast, dry_run)
    rel_paths = [os.path.relpath((cwd_p / p) if not os.path.isabs(p) else p, root) for p in paths]

    if rerun_failed and (root / RERUN_FILE).exists():
        rel_paths = ["@" + RERUN_FILE]

    def _exec(cmd, out_stream=False):
        return subprocess.run(cmd, cwd=str(root), env=child_env, timeout=timeout,
                              capture_output=not out_stream, text=True)

    output = ""
    if parallel:
        files = _feature_files(rel_paths, root) if not rel_paths[0].startswith("@") else []
        if not files:
            parallel = False
    if parallel:
        results = []

        def one(i_f):
            i, f = i_f
            part = out_dir / f"result_{i}.json"
            cmd = cmd_base + ["-f", JSON_FORMATTER, "-o", str(part), "-f", "progress", str(f)]
            r = _exec(cmd)
            return r.returncode, (r.stdout or "") + (r.stderr or ""), part

        with ThreadPoolExecutor(max_workers=max(1, workers)) as ex:
            results = list(ex.map(one, enumerate(files)))
        returncode = 0 if all(rc == 0 for rc, _, _ in results) else 1
        output = "\n".join(o for _, o, _ in results)
        merged = {"summary": {"features": 0, "scenarios": 0, "passed": 0, "failed": 0, "skipped": 0},
                  "features": []}
        for _, _, part in results:
            if part.exists():
                data = json.loads(part.read_text(encoding="utf-8"))
                for k, v in data["summary"].items():
                    merged["summary"][k] += v
                merged["features"].extend(data["features"])
                part.unlink()
        result_file.write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8")
    else:
        cmd = cmd_base + ["-f", JSON_FORMATTER, "-o", str(result_file),
                          "-f", "rerun", "-o", str(root / RERUN_FILE)]
        if fmt != "json":
            cmd += ["-f", "pretty" if verbose else "progress"]
        if junit:
            cmd += ["--junit", "--junit-directory", str(out_dir / "junit")]
        cmd += rel_paths
        r = _exec(cmd, out_stream=stream)
        returncode = r.returncode
        output = "" if stream else (r.stdout or "") + (r.stderr or "")
        attempt = 0
        while returncode != 0 and attempt < retries and (root / RERUN_FILE).exists() \
                and (root / RERUN_FILE).read_text(encoding="utf-8").strip() and not dry_run:
            attempt += 1
            retry_file = out_dir / f"result_retry_{attempt}.json"
            rcmd = cmd_base + ["-f", JSON_FORMATTER, "-o", str(retry_file),
                               "-f", "rerun", "-o", str(root / (RERUN_FILE + ".next")), "@" + RERUN_FILE]
            rr = _exec(rcmd)
            nxt = root / (RERUN_FILE + ".next")
            if nxt.exists():  # the retry's own failures become the next rerun list
                nxt.replace(root / RERUN_FILE)
            returncode = rr.returncode
            output += f"\n--- retry {attempt} ---\n" + (rr.stdout or "") + (rr.stderr or "")
            if retry_file.exists():
                _merge_retry(result_file, retry_file, attempt)
                retry_file.unlink()

    summary = None
    if result_file.exists():
        try:
            summary = json.loads(result_file.read_text(encoding="utf-8")).get("summary")
        except ValueError:
            summary = None
    return {"returncode": returncode, "passed": returncode == 0, "summary": summary,
            "result_file": str(result_file), "output": output, "root": str(root)}


def _merge_retry(main: Path, retry: Path, attempt: int) -> None:
    """Replace failed scenarios in ``main`` by their retry outcome (marks them ``retried``)."""
    base = json.loads(main.read_text(encoding="utf-8"))
    again = json.loads(retry.read_text(encoding="utf-8"))
    fresh = {(f["file"], s["name"]): s for f in again["features"] for s in f["scenarios"]}
    for f in base["features"]:
        for i, s in enumerate(f["scenarios"]):
            new = fresh.get((f["file"], s["name"]))
            if new is not None and s["status"] == "failed":
                new["retried"] = attempt
                f["scenarios"][i] = new
    scs = [s for f in base["features"] for s in f["scenarios"]]
    base["summary"].update(
        scenarios=len(scs), passed=sum(s["status"] == "passed" for s in scs),
        failed=sum(s["status"] == "failed" for s in scs),
        skipped=sum(s["status"] not in ("passed", "failed") for s in scs))
    base["summary"]["flaky"] = sum(1 for s in scs if s.get("retried") and s["status"] == "passed")
    main.write_text(json.dumps(base, indent=2, ensure_ascii=False), encoding="utf-8")


def load_result(path: str, only_failures: bool = False, compact: bool = False) -> Dict:
    """compact: drop step lists of passed scenarios (keeps AI/CI output small)."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if compact:
        for f in data["features"]:
            for s in f["scenarios"]:
                if s["status"] == "passed":
                    s["steps"] = len(s["steps"])
    if only_failures:
        feats = []
        for f in data["features"]:
            sc = [s for s in f["scenarios"] if s["status"] == "failed"]
            if sc:
                feats.append({**f, "scenarios": sc})
        data = {"summary": data["summary"], "features": feats}
    return data
