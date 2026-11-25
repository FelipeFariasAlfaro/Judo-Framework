"""
Last HTTP exchange store and secret masking.

``make_request`` records the most recent request/response here so that the JSON
formatter and the MCP server can show failures with full context, without
leaking credentials.
"""
import copy
import re
from typing import Any, Dict, Optional

_SENSITIVE_HEADERS = {
    "authorization", "proxy-authorization", "cookie", "set-cookie",
    "x-api-key", "api-key", "x-auth-token", "x-access-token",
}
_SENSITIVE_KEY_RE = re.compile(
    r"(pass(word)?|secret|token|api[_-]?key|authorization|credential|private[_-]?key)", re.I)
MASK = "***"

_last: Dict[str, Optional[Dict[str, Any]]] = {"request": None, "response": None}


def mask_secrets(value: Any) -> Any:
    """Recursively mask sensitive keys in dicts/lists (returns a copy)."""
    if isinstance(value, dict):
        out = {}
        for k, v in value.items():
            if isinstance(k, str) and (k.lower() in _SENSITIVE_HEADERS or _SENSITIVE_KEY_RE.search(k)):
                out[k] = MASK
            else:
                out[k] = mask_secrets(v)
        return out
    if isinstance(value, list):
        return [mask_secrets(v) for v in value]
    return value


def record(request: Optional[dict], response: Optional[dict]) -> None:
    _last["request"] = copy.deepcopy(request) if request is not None else None
    _last["response"] = copy.deepcopy(response) if response is not None else None


def last_exchange(mask: bool = True) -> Dict[str, Any]:
    data = {"request": _last["request"], "response": _last["response"]}
    return mask_secrets(data) if mask else data


def clear() -> None:
    _last["request"] = None
    _last["response"] = None
