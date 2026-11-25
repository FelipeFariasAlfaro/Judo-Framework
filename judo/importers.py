"""
Importers: turn curl commands, OpenAPI specs and Postman collections into
Judo ``.feature`` drafts. They only emit steps that exist in the framework.
"""
import json
import shlex
from typing import Any, Dict, List, Optional
from urllib.parse import urlsplit

from .utils.exchange import mask_secrets

_METHODS = ("get", "post", "put", "patch", "delete")
_BODY_METHODS = ("POST", "PUT", "PATCH")


def _esc(value: Any) -> str:
    return str(value).replace('"', '\\"')


def _scenario(name: str, method: str, path: str, headers: Dict[str, str],
              body: Optional[Any], expected_status: Any, auth_bearer: Optional[str] = None,
              tags: Optional[List[str]] = None) -> List[str]:
    method = method.upper()
    lines = []
    if tags:
        lines.append("  " + " ".join(f"@{t}" for t in tags))
    lines.append(f"  Scenario: {name}")
    for k, v in headers.items():
        if k.lower() == "authorization" and v.lower().startswith("bearer "):
            auth_bearer = v[7:]
            continue
        if k.lower() == "authorization":
            lines.append(f'    Given I set the header "{_esc(k)}" to "${{AUTH_HEADER}}"')
            continue
        lines.append(f'    Given I set the header "{_esc(k)}" to "{_esc(v)}"')
    if auth_bearer is not None:
        lines.append(f'    And I use bearer token "{_esc(auth_bearer)}"')
    if body is not None and method in _BODY_METHODS:
        text = body if isinstance(body, str) else json.dumps(body, indent=2, ensure_ascii=False)
        lines.append(f'    When I send a {method} request to "{_esc(path)}" with JSON')
        lines.append('      """')
        lines.extend("      " + l for l in text.splitlines())
        lines.append('      """')
    elif method == "GET":
        lines.append(f'    When I send a GET request to "{_esc(path)}"')
    elif method == "DELETE":
        lines.append(f'    When I send a DELETE request to "{_esc(path)}"')
    elif method == "POST":
        lines.append(f'    When I send a POST request to "{_esc(path)}"')
    else:
        lines.append(f'    When I send a {method} request to "{_esc(path)}" with JSON')
        lines.append('      """')
        lines.append("      {}")
        lines.append('      """')
    if isinstance(expected_status, (list, tuple)):
        codes = ",".join(str(c) for c in expected_status)
        lines.append(f'    Then the response status should be one of "{codes}"')
    else:
        lines.append(f"    Then the response status should be {expected_status}")
    return lines


def _feature(title: str, base_url: Optional[str], scenarios: List[List[str]]) -> str:
    out = [f"Feature: {title}", ""]
    if base_url:
        out += ["  Background:", "    Given I have a Judo API client",
                f'    And the base URL is "{_esc(base_url)}"', ""]
    for sc in scenarios:
        out += sc + [""]
    return "\n".join(out).rstrip() + "\n"


# ---------------------------------------------------------------------------
# curl
# ---------------------------------------------------------------------------
def from_curl(command: str) -> str:
    """Convert a curl command into a feature draft (secrets are masked)."""
    tokens = shlex.split(command.replace("\\\n", " "))
    if tokens and tokens[0] == "curl":
        tokens = tokens[1:]
    method, url, data = None, None, None
    headers: Dict[str, str] = {}
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t in ("-X", "--request"):
            method = tokens[i + 1]; i += 1
        elif t in ("-H", "--header"):
            k, _, v = tokens[i + 1].partition(":")
            headers[k.strip()] = v.strip(); i += 1
        elif t in ("-d", "--data", "--data-raw", "--data-binary", "--json"):
            data = tokens[i + 1]; i += 1
        elif t in ("-u", "--user"):
            headers["Authorization"] = "Basic ${BASIC_AUTH}"; i += 1
        elif not t.startswith("-") and url is None:
            url = t
        i += 1
    if not url:
        raise ValueError("No URL found in curl command")
    parts = urlsplit(url)
    path = parts.path or "/"
    if parts.query:
        path += "?" + parts.query
    base = f"{parts.scheme}://{parts.netloc}" if parts.scheme else None
    method = (method or ("POST" if data else "GET")).upper()
    body: Any = data
    if data:
        try:
            body = json.loads(data)
        except ValueError:
            pass
    if isinstance(body, dict):
        body = mask_secrets(body)
    bearer = None
    for k in list(headers):
        if k.lower() == "authorization" and headers[k].lower().startswith("bearer "):
            bearer = "${TOKEN}"
            del headers[k]
    sc = _scenario(f"{method} {parts.path or '/'}", method, path, headers, body, 200, auth_bearer=bearer)
    return _feature(f"Imported from curl: {method} {parts.path or '/'}", base, [sc])


# ---------------------------------------------------------------------------
# OpenAPI 3 / Swagger 2
# ---------------------------------------------------------------------------
def _example_from_schema(schema: Dict[str, Any], spec: Dict[str, Any], depth: int = 0) -> Any:
    if not isinstance(schema, dict) or depth > 4:
        return None
    if "$ref" in schema:
        node: Any = spec
        for part in schema["$ref"].lstrip("#/").split("/"):
            node = node.get(part, {}) if isinstance(node, dict) else {}
        return _example_from_schema(node, spec, depth + 1)
    if "example" in schema:
        return schema["example"]
    if "default" in schema:
        return schema["default"]
    if schema.get("enum"):
        return schema["enum"][0]
    t = schema.get("type")
    if t == "object" or "properties" in schema:
        return {k: _example_from_schema(v, spec, depth + 1)
                for k, v in (schema.get("properties") or {}).items()}
    if t == "array":
        return [_example_from_schema(schema.get("items", {}), spec, depth + 1)]
    return {"string": "string", "integer": 1, "number": 1.5, "boolean": True}.get(t, "string")


def _resolve(schema: Dict[str, Any], spec: Dict[str, Any]) -> Dict[str, Any]:
    depth = 0
    while isinstance(schema, dict) and "$ref" in schema and depth < 10:
        node: Any = spec
        for part in schema["$ref"].lstrip("#/").split("/"):
            node = node.get(part, {}) if isinstance(node, dict) else {}
        schema, depth = node, depth + 1
    return schema if isinstance(schema, dict) else {}


def _negative_scenarios(name: str, method: str, path: str, raw_path: str, body: Any,
                        schema: Dict[str, Any], spec: Dict[str, Any], tags: List[str]) -> List[List[str]]:
    """Negative / edge cases derived from the schema: missing required, wrong type, empty body, unknown id."""
    out: List[List[str]] = []
    neg_tags = tags + ["negative"]
    schema = _resolve(schema, spec)
    props = schema.get("properties") or {}
    if method.upper() in _BODY_METHODS and isinstance(body, dict):
        for field in (schema.get("required") or [])[:3]:
            if field in body:
                broken = {k: v for k, v in body.items() if k != field}
                out.append(_scenario(f"{name} - missing required '{field}'", method, path, {}, broken,
                                     [400, 422], tags=neg_tags))
        for field, fs in list(props.items())[:5]:
            t = _resolve(fs, spec).get("type")
            if field in body and t in ("string", "integer", "number", "boolean"):
                wrong = {"string": 12345, "integer": "not-a-number", "number": "not-a-number", "boolean": "maybe"}[t]
                out.append(_scenario(f"{name} - wrong type for '{field}'", method, path, {}, {**body, field: wrong},
                                     [400, 422], tags=neg_tags))
                break
        if schema.get("required"):
            out.append(_scenario(f"{name} - empty body", method, path, {}, {}, [400, 422], tags=neg_tags))
    if raw_path != path and method.upper() in ("GET", "PUT", "PATCH", "DELETE"):
        import re as _re
        ghost = _re.sub(r"\{[^}]+\}", "999999999", raw_path)
        out.append(_scenario(f"{name} - unknown resource", method, ghost, {},
                             body if method.upper() in _BODY_METHODS else None, [404, 400], tags=neg_tags))
    return out


def from_openapi(spec: Dict[str, Any], tag_filter: Optional[str] = None, negative: bool = False) -> str:
    """Convert an OpenAPI/Swagger spec into a feature with one happy-path scenario per operation.
    With ``negative=True`` it also generates negative cases (missing/wrong fields, unknown ids)."""
    title = (spec.get("info") or {}).get("title", "API")
    base = None
    if spec.get("servers"):
        base = spec["servers"][0].get("url")
    elif spec.get("host"):
        base = f"{(spec.get('schemes') or ['https'])[0]}://{spec['host']}{spec.get('basePath', '')}"
    scenarios = []
    for path, item in (spec.get("paths") or {}).items():
        for method in _METHODS:
            op = (item or {}).get(method)
            if not op:
                continue
            if tag_filter and tag_filter not in (op.get("tags") or []):
                continue
            real_path = path
            for p in (op.get("parameters") or []) + (item.get("parameters") or []):
                if p.get("in") == "path":
                    ex = p.get("example", (p.get("schema") or {}).get("example", 1))
                    real_path = real_path.replace("{" + p["name"] + "}", str(ex))
            body = None
            rb = (op.get("requestBody") or {}).get("content", {}).get("application/json")
            if rb:
                body = rb.get("example") or _example_from_schema(rb.get("schema", {}), spec)
            else:
                for p in op.get("parameters") or []:
                    if p.get("in") == "body":
                        body = _example_from_schema(p.get("schema", {}), spec)
            codes = [c for c in (op.get("responses") or {}) if str(c).isdigit() and str(c).startswith("2")]
            status = int(sorted(codes)[0]) if codes else 200
            name = op.get("summary") or op.get("operationId") or f"{method.upper()} {path}"
            tags = [t.replace(" ", "_") for t in (op.get("tags") or [])[:1]]
            scenarios.append(_scenario(name, method, real_path, {}, body, status, tags=tags))
            if negative:
                schema = (rb or {}).get("schema", {}) if rb else next(
                    (p.get("schema", {}) for p in op.get("parameters") or [] if p.get("in") == "body"), {})
                scenarios.extend(_negative_scenarios(name, method, real_path, path, body, schema, spec, tags))
    if not scenarios:
        raise ValueError("No operations found in the OpenAPI spec")
    return _feature(title, base, scenarios)


# ---------------------------------------------------------------------------
# Postman collection v2.x
# ---------------------------------------------------------------------------
def _walk_postman(items: List[Dict[str, Any]]):
    for it in items:
        if "item" in it:
            yield from _walk_postman(it["item"])
        elif "request" in it:
            yield it


def from_postman(collection: Dict[str, Any]) -> str:
    title = (collection.get("info") or {}).get("name", "Postman collection")
    scenarios = []
    base = None
    for it in _walk_postman(collection.get("item", [])):
        req = it["request"]
        if isinstance(req, str):
            continue
        url = req.get("url", "")
        raw = url if isinstance(url, str) else url.get("raw", "")
        parts = urlsplit(raw.replace("{{", "${").replace("}}", "}"))
        path = (parts.path or "/") + (f"?{parts.query}" if parts.query else "")
        if base is None and parts.netloc:
            base = f"{parts.scheme}://{parts.netloc}"
        headers = {h["key"]: h.get("value", "") for h in req.get("header", []) if not h.get("disabled")}
        body = None
        raw_body = (req.get("body") or {}).get("raw")
        if raw_body:
            try:
                body = json.loads(raw_body)
            except ValueError:
                body = raw_body
        scenarios.append(_scenario(it.get("name", path), req.get("method", "GET"), path, headers, body, 200))
    if not scenarios:
        raise ValueError("No requests found in the Postman collection")
    return _feature(title, base, scenarios)


def from_file(kind: str, path: str, tag_filter: Optional[str] = None, negative: bool = False) -> str:
    """kind: curl | openapi | postman"""
    with open(path, "r", encoding="utf-8") as fh:
        raw = fh.read()
    if kind == "curl":
        return from_curl(raw)
    if path.endswith((".yaml", ".yml")):
        import yaml
        data = yaml.safe_load(raw)
    else:
        data = json.loads(raw)
    if kind == "openapi":
        return from_openapi(data, tag_filter, negative)
    if kind == "postman":
        return from_postman(data)
    raise ValueError(f"Unknown import kind: {kind}")
