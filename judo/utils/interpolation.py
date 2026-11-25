"""
Variable interpolation engine (single implementation for all steps).

Supported syntax
  ${name}                 variable
  ${name:-default}        default when the variable is missing
  ${user.address.city}    nested access, ${items[0].id} for lists
  ${env.NAME}             environment variable
  ${uuid()}  ${now()}  ${timestamp()}  ${random_int(1,100)}  ${random_string(8)}
  {name}                  legacy form: only replaced when ``name`` is a known variable
                          (so JSON braces in bodies are never touched)

Unknown ``${...}`` expressions are left untouched, unless strict mode is on
(``JUDO_STRICT_VARS=true`` or ``strict=True``): then a clear error lists the known variables.
"""
import json
import os
import random
import re
import string
import time
import uuid as _uuid
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Optional

_EXPR = re.compile(r"\$\{([^{}]+)\}")
_LEGACY = re.compile(r"\{([A-Za-z_][\w.\[\]]*)\}")
_FUNC = re.compile(r"^(\w+)\((.*)\)$")
_PATH_TOKEN = re.compile(r"([^.\[\]]+)|\[(\d+)\]")

_MISSING = object()


def _functions() -> Dict[str, Callable]:
    return {
        "uuid": lambda: str(_uuid.uuid4()),
        "now": lambda: datetime.now(timezone.utc).isoformat(),
        "timestamp": lambda: int(time.time()),
        "random_int": lambda a=0, b=100: random.randint(int(a), int(b)),
        "random_string": lambda n=10: "".join(random.choices(string.ascii_letters + string.digits, k=int(n))),
    }


def _walk(root: Any, path: str) -> Any:
    cur = root
    for name, idx in _PATH_TOKEN.findall(path):
        if idx != "":
            if not isinstance(cur, (list, tuple)) or int(idx) >= len(cur):
                return _MISSING
            cur = cur[int(idx)]
        elif isinstance(cur, dict) and name in cur:
            cur = cur[name]
        else:
            return _MISSING
    return cur


def resolve(expr: str, variables: Dict[str, Any]) -> Any:
    """Resolve one expression (without ``${}``); returns ``_MISSING`` when unknown."""
    expr = expr.strip()
    default = _MISSING
    if ":-" in expr:
        expr, default = expr.split(":-", 1)
        expr = expr.strip()
    value: Any = _MISSING
    m = _FUNC.match(expr)
    if m and m.group(1) in _functions():
        args = [a.strip().strip("'\"") for a in m.group(2).split(",") if a.strip()]
        value = _functions()[m.group(1)](*args)
    elif expr.startswith("env."):
        value = os.environ.get(expr[4:], _MISSING)
    elif expr in variables:
        value = variables[expr]
    else:
        root = re.split(r"[.\[]", expr, 1)[0]
        if root in variables and root != expr:
            value = _walk(variables[root], expr[len(root):].lstrip("."))
    if value is _MISSING:
        return default
    return value


def _to_text(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def strict_enabled() -> bool:
    return os.getenv("JUDO_STRICT_VARS", "false").lower() == "true"


def interpolate(text: Any, variables: Dict[str, Any], strict: Optional[bool] = None) -> Any:
    """Interpolate ``text`` (non-strings are returned unchanged)."""
    if not isinstance(text, str) or ("{" not in text):
        return text
    strict = strict_enabled() if strict is None else strict

    def repl_expr(m: "re.Match") -> str:
        value = resolve(m.group(1), variables)
        if value is _MISSING:
            if strict:
                known = ", ".join(sorted(variables)) or "(none)"
                raise AssertionError(f"Undefined variable '${{{m.group(1)}}}'. Known variables: {known}")
            return m.group(0)
        return _to_text(value)

    out = _EXPR.sub(repl_expr, text)

    def repl_legacy(m: "re.Match") -> str:
        name = m.group(1)
        if name in variables:
            return _to_text(variables[name])
        root = re.split(r"[.\[]", name, 1)[0]
        if root in variables and root != name:
            value = _walk(variables[root], name[len(root):].lstrip("."))
            if value is not _MISSING:
                return _to_text(value)
        return m.group(0)

    out = _LEGACY.sub(repl_legacy, out)
    # Backward compatibility: variable names with characters outside [A-Za-z0-9_.]
    for key, value in variables.items():
        if isinstance(key, str) and not re.fullmatch(r"[A-Za-z_][\w]*", key):
            out = out.replace("${" + key + "}", _to_text(value)).replace("{" + key + "}", _to_text(value))
    return out
