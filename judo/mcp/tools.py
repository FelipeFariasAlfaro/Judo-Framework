"""
Plain-Python implementations of the Judo MCP tools (no MCP SDK required),
so they can be unit tested and reused. ``server.py`` only registers them.

Security model
- ``send_request`` only reaches hosts in JUDO_MCP_ALLOWED_HOSTS (comma separated,
  ``*`` allows any). Default: localhost only.
- File access is confined to JUDO_MCP_WORKDIR (default: current directory).
- Secrets (tokens, passwords, auth headers) are masked in every output.
"""
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlsplit

from .. import importers
from ..runner import cli_runner
from ..utils import step_catalog as sc
from ..utils.exchange import mask_secrets
from ..utils.feature_validator import validate_feature_text, validate_paths

_mocks: Dict[int, Any] = {}


def workdir() -> Path:
    return Path(os.environ.get("JUDO_MCP_WORKDIR", os.getcwd())).resolve()


def _safe_path(rel: str) -> Path:
    base = workdir()
    p = (base / rel).resolve() if not os.path.isabs(rel) else Path(rel).resolve()
    if base != p and base not in p.parents:
        raise PermissionError(f"Path outside the working directory ({base}): {rel}")
    return p


def _catalog() -> List[Dict]:
    cat = sc.load_catalog()
    for d in (workdir() / "features" / "steps", workdir() / "steps"):
        cat += sc.load_project_steps(d)
    return cat


# ---------------------------------------------------------------------------
# Step discovery
# ---------------------------------------------------------------------------
def search_steps(query: str, lang: Optional[str] = None, category: Optional[str] = None,
                 limit: int = 15) -> Dict:
    results = sc.search_steps(query, _catalog(), lang=lang, category=category, limit=limit)
    return {"count": len(results), "steps": results}


def list_step_categories() -> Dict:
    cat = _catalog()
    return {"total": len(cat), "categories": sc.categories(cat),
            "languages": {l: sum(1 for s in cat if s["lang"] == l) for l in ("en", "es")}}


def get_step(pattern: str) -> Dict:
    for s in sc.public_catalog(_catalog()):
        if s["pattern"] == pattern:
            return s
    return {"error": "Step not found", "suggestions": sc.suggest(pattern, _catalog())}


# ---------------------------------------------------------------------------
# Feature authoring
# ---------------------------------------------------------------------------
def draft_feature(source_type: str, content: str, tag_filter: Optional[str] = None,
                  negative: bool = False) -> Dict:
    """source_type: curl | openapi | postman. ``content`` is raw text (curl, JSON or YAML)."""
    if source_type == "curl":
        text = importers.from_curl(content)
    else:
        try:
            data = json.loads(content)
        except ValueError:
            import yaml
            data = yaml.safe_load(content)
        text = importers.from_openapi(data, tag_filter, negative) if source_type == "openapi" \
            else importers.from_postman(data)
    issues = validate_feature_text(text, _catalog())
    return {"feature": text, "issues": issues}


def validate_feature(path: Optional[str] = None, text: Optional[str] = None) -> Dict:
    if text is not None:
        issues = validate_feature_text(text, _catalog())
        errors = [i for i in issues if i["severity"] == "error"]
        return {"ok": not errors, "errors": len(errors), "issues": issues}
    return validate_paths([str(_safe_path(path or "features"))])


def write_feature(path: str, content: str, overwrite: bool = False) -> Dict:
    if not path.endswith(".feature"):
        raise ValueError("Only .feature files can be written")
    target = _safe_path(path)
    if target.exists() and not overwrite:
        return {"written": False, "reason": "File exists. Pass overwrite=true to replace it."}
    check = validate_feature(text=content)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return {"written": True, "path": str(target), "validation": check}


# ---------------------------------------------------------------------------
# Execution
# ---------------------------------------------------------------------------
def run_tests(path: str = "features", tags: Optional[List[str]] = None, env: Optional[str] = None,
              rerun_failed: bool = False, fail_fast: bool = False, parallel: bool = False,
              dry_run: bool = False) -> Dict:
    res = cli_runner.run_tests([str(_safe_path(path))], tags=tags, env=env, rerun_failed=rerun_failed,
                               fail_fast=fail_fast, parallel=parallel, dry_run=dry_run,
                               cwd=str(workdir()), fmt="json", timeout=900)
    out: Dict[str, Any] = {"passed": res["passed"], "returncode": res["returncode"],
                           "summary": res["summary"], "result_file": res["result_file"]}
    if Path(res["result_file"]).exists():
        out["failures"] = cli_runner.load_result(res["result_file"], only_failures=True)["features"]
    if not res["summary"]:
        out["output"] = res["output"][-3000:]
    return out


def explain_failure() -> Dict:
    """Classify the failures of the last run: probable cause, evidence and next action."""
    from .. import diagnose
    report = get_last_report(only_failures=True, compact=False)
    if "error" in report:
        return report
    return diagnose.explain(report)


def api_coverage(spec_path: str, features_path: str = "features") -> Dict:
    """Which OpenAPI operations are exercised by the feature files."""
    from .. import coverage
    spec = coverage.load_spec(str(_safe_path(spec_path)))
    return coverage.compute(spec, [str(_safe_path(features_path))])


def guide() -> str:
    from ..ai_templates import render_guide
    return render_guide()


def get_last_report(only_failures: bool = False, compact: bool = True) -> Dict:
    for p in (workdir() / "judo_reports" / "result.json",
              workdir() / "features" / "judo_reports" / "result.json"):
        if p.exists():
            return cli_runner.load_result(str(p), only_failures, compact)
    return {"error": "No result.json found. Run tests first."}


def list_reports() -> Dict:
    found = []
    for pat in ("judo_reports", "test_reports", "reports"):
        d = workdir() / pat
        if d.is_dir():
            for f in sorted(d.rglob("*"), key=lambda x: x.stat().st_mtime, reverse=True)[:30]:
                if f.is_file():
                    found.append(str(f.relative_to(workdir())))
    return {"reports": found}


# ---------------------------------------------------------------------------
# HTTP exploration
# ---------------------------------------------------------------------------
def _host_allowed(url: str) -> bool:
    host = urlsplit(url).hostname or ""
    allowed = [h.strip().lower() for h in os.environ.get(
        "JUDO_MCP_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if h.strip()]
    return "*" in allowed or host.lower() in allowed or any(
        host.lower().endswith("." + a.lstrip("*.")) for a in allowed if a.startswith("*."))


def send_request(method: str, url: str, headers: Optional[Dict[str, str]] = None,
                 body: Optional[Any] = None, timeout: int = 30) -> Dict:
    import requests
    if not _host_allowed(url):
        return {"error": f"Host not allowed: {urlsplit(url).hostname}. "
                         "Set JUDO_MCP_ALLOWED_HOSTS (comma separated, '*' for any)."}
    kwargs: Dict[str, Any] = {"headers": headers or {}, "timeout": timeout}
    if body is not None:
        kwargs["json" if not isinstance(body, str) else "data"] = body
    r = requests.request(method.upper(), url, **kwargs)
    try:
        payload: Any = r.json()
    except ValueError:
        payload = r.text[:5000]
    return mask_secrets({"status": r.status_code, "elapsed_ms": round(r.elapsed.total_seconds() * 1000, 1),
                         "headers": dict(r.headers), "body": payload,
                         "request": {"method": method.upper(), "url": url, "headers": headers or {}}})


# ---------------------------------------------------------------------------
# Environment and mock
# ---------------------------------------------------------------------------
def get_env() -> Dict:
    """Judo-related environment variables, secrets masked."""
    keep = re.compile(r"^(JUDO_|KARATE_|BASE_URL|API_)")
    env = {k: v for k, v in os.environ.items() if keep.match(k)}
    return {"workdir": str(workdir()), "env": mask_secrets(env),
            "env_file": (workdir() / ".env").exists()}


def start_mock(port: int = 8089, routes: Optional[List[Dict]] = None) -> Dict:
    """routes: [{"method": "GET", "path": "/ping", "status": 200, "body": {...}}]"""
    from ..mock.server import MockServer
    if port in _mocks:
        return {"error": f"Mock already running on port {port}"}
    srv = MockServer(port)
    for r in routes or [{"method": "GET", "path": "/health", "status": 200, "body": {"status": "ok"}}]:
        srv.add_route(r.get("method", "GET"), r["path"],
                      {"status": r.get("status", 200), "body": r.get("body", {})})
    srv.start()
    _mocks[port] = srv
    return {"running": True, "url": f"http://localhost:{port}"}


def stop_mock(port: int = 8089) -> Dict:
    srv = _mocks.pop(port, None)
    if not srv:
        return {"error": f"No mock on port {port}"}
    srv.stop()
    return {"stopped": True}
