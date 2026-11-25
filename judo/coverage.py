"""
API coverage: which OpenAPI operations are exercised by the feature files.

A feature "covers" an operation when it sends the same HTTP method to a path that
matches the spec's path template (``/users/{id}`` matches ``/users/7`` or ``/users/${id}``).
"""
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

_METHODS = ("get", "post", "put", "patch", "delete", "head", "options")
_REQ_STEP = re.compile(
    r"""(?:send\s+an?\s+(?P<m1>[A-Z]+)\s+request\s+to|I\s+(?P<m2>GET|POST|PUT|PATCH|DELETE)\s+to|"""
    r"""hago\s+una\s+petici[oó]n\s+(?P<m3>[A-Z]+)\s+a|hago\s+(?P<m4>POST|PUT|PATCH)\s+a|"""
    r"""env[ií]o\s+una\s+petici[oó]n\s+(?P<m5>[A-Z]+)\s+a|send\s+(?:\d+\s+)(?P<m6>GET)\s+requests\s+to)\s+"(?P<path>[^"]+)\"""",
    re.IGNORECASE)


def _template_regex(template: str) -> "re.Pattern":
    parts = re.split(r"\{[^}]+\}", template)
    return re.compile("^" + r"[^/]+".join(re.escape(p) for p in parts) + "/?$")


def spec_operations(spec: Dict) -> List[Tuple[str, str]]:
    ops = []
    for path, item in (spec.get("paths") or {}).items():
        for m in _METHODS:
            if m in (item or {}):
                ops.append((m.upper(), path))
    return ops


def used_requests(feature_paths: List[str]) -> Set[Tuple[str, str]]:
    used: Set[Tuple[str, str]] = set()
    files: List[Path] = []
    for p in feature_paths:
        path = Path(p)
        files.extend(sorted(path.rglob("*.feature")) if path.is_dir() else [path])
    for f in files:
        for line in f.read_text(encoding="utf-8").splitlines():
            m = _REQ_STEP.search(line)
            if m:
                method = next(v for k, v in m.groupdict().items() if k.startswith("m") and v)
                path = m.group("path").split("?")[0]
                path = re.sub(r"\$?\{[^}]+\}", "1", path)
                used.add((method.upper(), path))
    return used


def compute(spec: Dict, feature_paths: List[str]) -> Dict:
    ops = spec_operations(spec)
    used = used_requests(feature_paths)
    covered, missing = [], []
    for method, template in ops:
        rx = _template_regex(template)
        hit = any(um == method and rx.match(up) for um, up in used)
        (covered if hit else missing).append(f"{method} {template}")
    total = len(ops)
    return {"total": total, "covered": len(covered),
            "percent": round(100.0 * len(covered) / total, 1) if total else 0.0,
            "missing": missing, "covered_operations": covered}


def load_spec(path: str) -> Dict:
    raw = Path(path).read_text(encoding="utf-8")
    if path.endswith((".yaml", ".yml")):
        import yaml
        return yaml.safe_load(raw)
    return json.loads(raw)
