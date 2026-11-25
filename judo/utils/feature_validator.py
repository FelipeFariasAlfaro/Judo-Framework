"""
Static validation of .feature files against the Judo step catalog.

No test is executed and behave is not required: each step line is matched
against known patterns (framework + project ``features/steps``). Unknown
steps get "did you mean" suggestions.
"""
import re
from pathlib import Path
from typing import Dict, List, Optional

from .step_catalog import (
    load_catalog, load_project_steps, match_step, strip_keyword, suggest,
)

_STRUCTURAL = re.compile(
    r"^\s*(Feature|Scenario Outline|Scenario Template|Scenario|Background|Examples|Rule|Example|"
    r"Caracter[ií]stica|Esquema del escenario|Escenario|Antecedentes|Ejemplos|Regla|Ejemplo)\s*:",
    re.IGNORECASE,
)


def _normalize(text: str) -> str:
    # Outline placeholders: <id> -> 1 when bare, keep inside quotes
    text = re.sub(r'(?<!")<[^<>"]+>(?!")', "1", text)
    return text


def iter_feature_files(paths: List[str]) -> List[Path]:
    files: List[Path] = []
    for p in paths or ["."]:
        path = Path(p)
        if path.is_dir():
            files.extend(sorted(path.rglob("*.feature")))
        elif path.suffix == ".feature" and path.exists():
            files.append(path)
    return files


def validate_feature_text(text: str, catalog: List[Dict], source: str = "<text>") -> List[Dict]:
    issues: List[Dict] = []
    in_doc = False
    last_is_flow = False
    doc_lines: List[str] = []
    doc_start = 0
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if line.startswith('"""') or line.startswith("```"):
            if not in_doc:
                doc_lines, doc_start = [], n
            elif last_is_flow:
                # a block of steps passed to a conditional/loop step: validate the nested steps too
                for issue in validate_feature_text("\n".join(doc_lines).replace("'''", '"""'), catalog, source):
                    issue["line"] += doc_start
                    issues.append(issue)
            in_doc = not in_doc
            continue
        if in_doc:
            doc_lines.append(raw)
            continue
        if not line or line.startswith(("#", "@", "|")) or _STRUCTURAL.match(line):
            continue
        if not re.match(r"^(Given|When|Then|And|But|\*|Dado|Dada|Dados|Dadas|Cuando|Entonces|Y |Pero|E |Sea|Si )", line, re.I):
            continue  # free-text description
        step_text = _normalize(strip_keyword(line))
        hits = match_step(step_text, catalog)
        last_is_flow = bool(hits) and all(h["module"].startswith("behave/steps_flow") for h in hits)
        if not hits:
            issues.append({"file": source, "line": n, "severity": "error", "type": "undefined",
                           "step": step_text, "suggestions": suggest(step_text, catalog)})
        elif len({h["pattern"] for h in hits}) > 1:
            issues.append({"file": source, "line": n, "severity": "warning", "type": "ambiguous",
                           "step": step_text, "matches": sorted({h["pattern"] for h in hits})})
    return issues


def validate_paths(paths: List[str], steps_dir: Optional[str] = None) -> Dict:
    catalog = load_catalog()
    candidates = [Path(steps_dir)] if steps_dir else []
    for p in paths or ["."]:
        base = Path(p)
        base = base if base.is_dir() else base.parent
        candidates += [base / "steps", base / "features" / "steps", base.parent / "steps"]
    seen = set()
    for c in candidates:
        if c.is_dir() and c.resolve() not in seen:
            seen.add(c.resolve())
            catalog += load_project_steps(c)
    files = iter_feature_files(paths)
    issues: List[Dict] = []
    for f in files:
        issues.extend(validate_feature_text(f.read_text(encoding="utf-8"), catalog, str(f)))
    errors = [i for i in issues if i["severity"] == "error"]
    return {"files": len(files), "errors": len(errors),
            "warnings": len(issues) - len(errors), "ok": not errors, "issues": issues}
