"""
Step catalog: single source of truth for every Judo step.

Steps are discovered statically (via ``ast``) from the step modules, so the
catalog never drifts from the code and never needs behave to be imported.
Used by ``judo steps``, ``judo validate`` and the MCP server.
"""
import ast
import difflib
import re
from pathlib import Path
from typing import Dict, List, Optional

_DECORATORS = {"step", "given", "when", "then"}

# module file (relative to the ``judo`` package) -> (language, category)
_STEP_MODULES = {
    "behave/steps.py": "en",
    "behave/steps_es.py": "es",
    "genai/steps_genai.py": "en",
    "genai/steps_genai_es.py": "es",
    "behave/steps_extra.py": "en",
    "behave/steps_extra_es.py": "es",
    "behave/steps_flow.py": "en",
    "behave/steps_flow_es.py": "es",
    "behave/steps_protocols.py": "en",
    "behave/steps_protocols_es.py": "es",
    "behave/steps_grpc.py": "en",
    "behave/steps_grpc_es.py": "es",
}

_PARAM_RE = re.compile(r"\{([^}:]*)(?::[^}]*)?\}")


def _package_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _category_for(module: str, func_name: str, pattern: str) -> str:
    if "genai" in module:
        return "genai"
    if "steps_flow" in module:
        return "flow"
    if "steps_grpc" in module:
        return "grpc"
    text = f"{func_name} {pattern}".lower()
    if "steps_protocols" in module:
        for cat, words in (("sse", ("sse",)), ("graphql", ("graphql",)),
                           ("xml", ("xml", "soap", "xsd")), ("forms", ("form", "csv", "text", "download", "bytes", "size", "content type"))):
            if any(w in text for w in words):
                return cat
    rules = [
        ("auth", ("token", "auth", "oauth", "jwt", "bearer", "basic", "api key")),
        ("database", ("sql", "database", "query")),
        ("polling", ("eventually", "poll", "retry until")),
        ("reporting", ("report", "junit", "allure", "html")),
        ("mock", ("mock",)),
        ("performance", ("performance", "p95", "average response", "metrics")),
        ("resilience", ("circuit", "retry", "rate limit", "throttle", "chaos")),
        ("variables", ("variable", "save", "extract")),
        ("validation", ("should", "validate", "match", "contain", "schema", "assert")),
        ("request", ("send", "request", "header", "param", "body", "url")),
    ]
    for name, words in rules:
        if any(w in text for w in words):
            return name
    return "general"


def _extract(path: Path, lang: str, module: str) -> List[Dict]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError):
        return []
    steps = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        for dec in node.decorator_list:
            if not (isinstance(dec, ast.Call) and isinstance(dec.func, ast.Name)):
                continue
            if dec.func.id not in _DECORATORS or not dec.args:
                continue
            arg = dec.args[0]
            if not (isinstance(arg, ast.Constant) and isinstance(arg.value, str)):
                continue
            pattern = arg.value
            steps.append({
                "pattern": pattern,
                "lang": lang,
                "function": node.name,
                "module": module,
                "line": node.lineno,
                "category": _category_for(module, node.name, pattern),
                "description": (ast.get_docstring(node) or "").strip().split("\n")[0],
                "params": [p for p in _PARAM_RE.findall(pattern) if p],
            })
    return steps


def load_catalog(root: Optional[Path] = None) -> List[Dict]:
    """Return every step definition found in the package (and optional extra dirs)."""
    root = root or _package_root()
    catalog: List[Dict] = []
    for rel, lang in _STEP_MODULES.items():
        path = root / rel
        if path.exists():
            catalog.extend(_extract(path, lang, rel))
    try:  # third-party plugins (entry point group 'judo.plugins')
        from ..plugins import discover
        for p in discover():
            if p["file"].endswith(".py"):
                catalog.extend(_extract(Path(p["file"]), "es" if p["file"].endswith("_es.py") else "en",
                                        f"plugin:{p['name']}"))
    except Exception:
        pass
    return catalog


def load_project_steps(steps_dir: Path) -> List[Dict]:
    """Steps defined by the user project (``features/steps/*.py``)."""
    out: List[Dict] = []
    if steps_dir.is_dir():
        for py in sorted(steps_dir.rglob("*.py")):
            lang = "es" if py.stem.endswith("_es") else "en"
            out.extend(_extract(py, lang, str(py)))
    return out


def _pattern_to_regex(pattern: str) -> "re.Pattern":
    """Convert a behave 'parse' pattern into a regex for matching step text."""
    out, last = "", 0
    for m in re.finditer(r"\{([^}]*)\}", pattern):
        out += re.escape(pattern[last:m.start()])
        spec = m.group(1)
        fmt = spec.split(":", 1)[1] if ":" in spec else ""
        # Same number rules as the ``parse`` library used by behave:
        # {x:d} integer, {x:f} needs a decimal point (5.0, not 5), {x:g} any number.
        if fmt == "d":
            out += r"[-+]?\d+"
        elif fmt == "f":
            out += r"[-+]?\d*\.\d+"
        elif fmt == "g":
            out += r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?"
        else:
            out += r".+?"
        last = m.end()
    out += re.escape(pattern[last:])
    return re.compile("^" + out + "$", re.DOTALL)


_KEYWORDS = re.compile(
    r"^\s*(Given|When|Then|And|But|\*|Dado|Dada|Dados|Dadas|Cuando|Entonces|Y|Pero|E|Sea|Si)\s+",
    re.IGNORECASE,
)


def strip_keyword(line: str) -> str:
    return _KEYWORDS.sub("", line.strip(), count=1).strip()


def match_step(text: str, catalog: List[Dict]) -> List[Dict]:
    """All catalog entries whose pattern matches the step text."""
    hits = []
    for s in catalog:
        rx = s.get("_rx") or _pattern_to_regex(s["pattern"])
        s["_rx"] = rx
        if rx.match(text):
            hits.append(s)
    return hits


def _public(step: Dict) -> Dict:
    return {k: v for k, v in step.items() if not k.startswith("_")}


def search_steps(query: str, catalog: List[Dict], lang: Optional[str] = None,
                 category: Optional[str] = None, limit: int = 20) -> List[Dict]:
    """Keyword + fuzzy search over patterns and descriptions."""
    words = [w for w in re.split(r"\W+", query.lower()) if w]
    scored = []
    for s in catalog:
        if lang and s["lang"] != lang:
            continue
        if category and s["category"] != category:
            continue
        hay = f"{s['pattern']} {s['description']}".lower()
        if words:
            hits = sum(1 for w in words if w in hay)
            if hits == 0:
                continue
            score = hits / len(words)
            score += difflib.SequenceMatcher(None, query.lower(), s["pattern"].lower()).ratio() * 0.3
        else:
            score = 0.0
        scored.append((score, s))
    scored.sort(key=lambda t: (-t[0], t[1]["pattern"]))
    return [_public(s) for _, s in scored[:limit]]


def suggest(text: str, catalog: List[Dict], n: int = 3) -> List[str]:
    """Closest step patterns to an unknown step text."""
    patterns = [s["pattern"] for s in catalog]
    flat = [re.sub(r"\{[^}]*\}", "X", p) for p in patterns]
    probe = re.sub(r'"[^"]*"', '"X"', text)
    probe = re.sub(r"\b\d+\b", "X", probe)
    close = difflib.get_close_matches(probe, flat, n=n, cutoff=0.4)
    return [patterns[flat.index(c)] for c in close]


def categories(catalog: List[Dict]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for s in catalog:
        counts[s["category"]] = counts.get(s["category"], 0) + 1
    return dict(sorted(counts.items()))


def find_duplicates(catalog: List[Dict]) -> List[Dict]:
    """Patterns defined more than once within the same language (AmbiguousStep risk)."""
    seen: Dict = {}
    dups = []
    for s in catalog:
        key = (s["lang"], s["pattern"])
        if key in seen:
            dups.append({"pattern": s["pattern"], "lang": s["lang"],
                         "locations": [f"{seen[key]['module']}:{seen[key]['line']}",
                                       f"{s['module']}:{s['line']}"]})
        else:
            seen[key] = s
    return dups


def public_catalog(catalog: List[Dict]) -> List[Dict]:
    return [_public(s) for s in catalog]
