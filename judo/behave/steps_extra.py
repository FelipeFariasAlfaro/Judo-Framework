"""
Extra Judo steps (English): polling, SQL (SQLite) and pagination.

The logic lives in ``_*`` helpers that the Spanish module (``steps_extra_es``)
reuses, so both languages always behave identically.
"""
import sqlite3
import time
from behave import step

from .context import JudoContext


def _ctx(context) -> JudoContext:
    if not hasattr(context, "judo_context"):
        context.judo_context = JudoContext(context)
    return context.judo_context


# ---------------------------------------------------------------------------
# Shared implementations
# ---------------------------------------------------------------------------
def _poll(context, endpoint, predicate, description, seconds, interval=1.0):
    jc = _ctx(context)
    deadline = time.time() + seconds
    last = None
    attempts = 0
    while True:
        attempts += 1
        jc.make_request("GET", endpoint)
        try:
            last = predicate(jc)
            if last[0]:
                return
        except Exception as exc:  # response not ready / path missing: keep polling
            last = (False, f"error: {exc}")
        if time.time() >= deadline:
            raise AssertionError(
                f"Polling timed out after {seconds}s ({attempts} attempts) waiting for {description}. "
                f"Last observed: {last[1]}"
            )
        time.sleep(interval)


def _poll_json_equals(context, endpoint, json_path, expected, seconds):
    jc = _ctx(context)
    expected = jc.interpolate_string(expected)

    def predicate(c):
        actual = c.judo.json_path(c.response.json, json_path)
        return (str(actual) == str(expected), actual)

    _poll(context, endpoint, predicate, f'"{json_path}" == "{expected}"', seconds)


def _poll_status(context, endpoint, status, seconds):
    def predicate(c):
        return (c.response.status == status, c.response.status)

    _poll(context, endpoint, predicate, f"status {status}", seconds)


def _sql_conn(context):
    conn = getattr(context, "_judo_sql_conn", None)
    assert conn is not None, "No database connection. Connect to a SQLite database first."
    return conn


def _open_db(target):
    """sqlite path, sqlite:///path, postgresql://..., mysql://... (drivers imported lazily)."""
    from urllib.parse import urlsplit, unquote
    if "://" not in target:
        return sqlite3.connect(target)
    parts = urlsplit(target)
    scheme = parts.scheme.split("+")[0]
    if scheme == "sqlite":
        return sqlite3.connect(unquote(parts.path[1:]) or ":memory:")
    if scheme in ("postgresql", "postgres"):
        try:
            import psycopg2 as driver
            return driver.connect(target)
        except ImportError:
            try:
                import psycopg
                return psycopg.connect(target)
            except ImportError:
                raise AssertionError("PostgreSQL needs a driver: pip install psycopg2-binary")
    if scheme == "mysql":
        try:
            import pymysql
        except ImportError:
            raise AssertionError("MySQL needs a driver: pip install pymysql")
        return pymysql.connect(host=parts.hostname, port=parts.port or 3306, user=unquote(parts.username or ""),
                               password=unquote(parts.password or ""), database=parts.path.lstrip("/"))
    raise AssertionError(f"Unsupported database URL scheme: {scheme}")


def _sql_connect(context, path):
    path = _ctx(context).interpolate_string(path)
    old = getattr(context, "_judo_sql_conn", None)
    if old is not None:
        old.close()
    context._judo_sql_conn = _open_db(path)


def _sql_execute(context, sql):
    conn = _sql_conn(context)
    cur = conn.cursor()
    cur.execute(_ctx(context).interpolate_string(sql))
    conn.commit()


def _sql_rows(context, sql):
    conn = _sql_conn(context)
    cur = conn.cursor()
    cur.execute(_ctx(context).interpolate_string(sql))
    return cur.fetchall() if cur.description else []


def _sql_save_first(context, sql, variable):
    rows = _sql_rows(context, sql)
    assert rows, f"SQL query returned no rows: {sql}"
    _ctx(context).set_variable(variable, rows[0][0])


def _sql_assert_count(context, sql, count):
    rows = _sql_rows(context, sql)
    assert len(rows) == count, f"Expected {count} rows, got {len(rows)} for: {sql}"


def _sql_assert_value(context, sql, expected):
    rows = _sql_rows(context, sql)
    assert rows, f"SQL query returned no rows: {sql}"
    expected = _ctx(context).interpolate_string(expected)
    assert str(rows[0][0]) == str(expected), f"Expected '{expected}', got '{rows[0][0]}'"


def _items_of(body):
    if isinstance(body, list):
        return body
    if isinstance(body, dict):
        for key in ("items", "data", "results", "content"):
            if isinstance(body.get(key), list):
                return body[key]
    return []


def _collect_pages(context, endpoint, page_param, max_pages, variable):
    jc = _ctx(context)
    sep = "&" if "?" in endpoint else "?"
    collected = []
    for page in range(1, max_pages + 1):
        jc.make_request("GET", f"{endpoint}{sep}{page_param}={page}")
        assert jc.response.status < 400, f"Page {page} failed with status {jc.response.status}"
        items = _items_of(jc.response.json)
        if not items:
            break
        collected.extend(items)
    jc.set_variable(variable, collected)


# ---------------------------------------------------------------------------
# English steps
# ---------------------------------------------------------------------------
@step('I poll "{endpoint}" until the response "{json_path}" equals "{expected}" within {seconds:d} seconds')
def step_poll_json_equals(context, endpoint, json_path, expected, seconds):
    """Repeat GET until a JSON path equals the expected value or time runs out"""
    _poll_json_equals(context, endpoint, json_path, expected, seconds)


@step('I poll "{endpoint}" until the status is {status:d} within {seconds:d} seconds')
def step_poll_status(context, endpoint, status, seconds):
    """Repeat GET until the status code matches or time runs out"""
    _poll_status(context, endpoint, status, seconds)


@step('I connect to the SQLite database "{path}"')
def step_sql_connect(context, path):
    """Open a SQLite database for data setup and verification"""
    _sql_connect(context, path)


@step('I execute the SQL "{sql}"')
def step_sql_execute(context, sql):
    """Execute a SQL statement (INSERT, UPDATE, DELETE, DDL)"""
    _sql_execute(context, sql)


@step('I save the first value of the SQL query "{sql}" as "{variable}"')
def step_sql_save_first(context, sql, variable):
    """Run a SQL query and store the first column of the first row in a variable"""
    _sql_save_first(context, sql, variable)


@step('the SQL query "{sql}" should return {count:d} rows')
def step_sql_count(context, sql, count):
    """Validate the number of rows a SQL query returns"""
    _sql_assert_count(context, sql, count)


@step('the SQL query "{sql}" should return the value "{expected}"')
def step_sql_value(context, sql, expected):
    """Validate the first value returned by a SQL query"""
    _sql_assert_value(context, sql, expected)


@step('I collect all pages from "{endpoint}" using the "{page_param}" parameter up to {max_pages:d} pages as "{variable}"')
def step_collect_pages(context, endpoint, page_param, max_pages, variable):
    """Walk a paginated GET endpoint and store all items in a variable"""
    _collect_pages(context, endpoint, page_param, max_pages, variable)


# ---------------------------------------------------------------------------
# HTTP settings, files, headers, XML/SOAP, JSON compare (shared implementations)
# ---------------------------------------------------------------------------
import hashlib
import re
import json
import mimetypes
import os

_SECURITY_HEADERS = ("strict-transport-security", "x-content-type-options")


def _http(context):
    return _ctx(context).judo.http_client


def _set_timeout(context, seconds):
    _http(context).set_timeout(seconds)


def _disable_ssl(context):
    _http(context).set_verify_ssl(False)


def _use_ca_bundle(context, path):
    path = _ctx(context).interpolate_string(path)
    assert os.path.exists(path), f"CA bundle not found: {path}"
    _http(context).set_verify_ssl(path)


def _use_client_cert(context, cert, key):
    _http(context).set_client_cert(_ctx(context).interpolate_string(cert),
                                   _ctx(context).interpolate_string(key))


def _use_proxy(context, url):
    _http(context).set_proxy(_ctx(context).interpolate_string(url))


def _response(context):
    resp = _ctx(context).response
    assert resp is not None, "No response available. Make a request first."
    return resp


def _upload(context, path, field, endpoint):
    jc = _ctx(context)
    path = jc.interpolate_string(path)
    assert os.path.isfile(path), f"File not found: {path}"
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    with open(path, "rb") as fh:
        # Content-Type None removes the default JSON header so requests builds the multipart boundary
        jc.make_request("POST", endpoint, files={field: (os.path.basename(path), fh, mime)},
                        headers={"Content-Type": None})


def _assert_sha256(context, expected):
    digest = hashlib.sha256(_response(context).content).hexdigest()
    expected = _ctx(context).interpolate_string(expected).lower()
    assert digest == expected, f"SHA-256 mismatch: expected {expected}, got {digest}"


def _header(context, name):
    headers = _response(context).headers
    for k, v in headers.items():
        if k.lower() == name.lower():
            return v
    return None


def _assert_header_equals(context, name, value):
    actual = _header(context, name)
    assert actual is not None, f"Response header '{name}' not found"
    value = _ctx(context).interpolate_string(value)
    assert actual == value, f"Header '{name}': expected '{value}', got '{actual}'"


def _assert_header_exists(context, name):
    assert _header(context, name) is not None, f"Response header '{name}' not found"


def _assert_security_headers(context):
    missing = [h for h in _SECURITY_HEADERS if _header(context, h) is None]
    if _header(context, "x-frame-options") is None and "frame-ancestors" not in (_header(context, "content-security-policy") or ""):
        missing.append("x-frame-options (or CSP frame-ancestors)")
    nosniff = _header(context, "x-content-type-options")
    if nosniff is not None and nosniff.lower() != "nosniff":
        missing.append("x-content-type-options must be 'nosniff'")
    assert not missing, f"Missing/invalid security headers: {', '.join(missing)}"


def _xml_values(text, xpath):
    """Return the string values selected by ``xpath`` (lxml when installed, ElementTree otherwise)."""
    data = text.encode("utf-8") if isinstance(text, str) else text
    try:
        from lxml import etree
        root = etree.fromstring(data)
        nsmap = {k: v for k, v in (root.nsmap or {}).items() if k}
        found = root.xpath(xpath, namespaces=nsmap)
        found = found if isinstance(found, list) else [found]
        return [str(f) if not hasattr(f, "text") else (f.text or "").strip() for f in found]
    except ImportError:
        import xml.etree.ElementTree as ET
        root = ET.fromstring(data)
        attr = None
        path = xpath
        if "/@" in path:
            path, attr = path.rsplit("/@", 1)
        if path.endswith("/text()"):
            path = path[:-7]
        if path.startswith("//"):
            path = "." + path
        elif path.startswith("/"):
            segs = path.split("/")[2:]
            path = "./" + "/".join(segs) if segs else "."
        nodes = root.findall(path) if path != "." else [root]
        if attr:
            return [n.attrib.get(attr, "") for n in nodes if attr in n.attrib]
        return [(n.text or "").strip() for n in nodes]


def _assert_xml_value(context, xpath, expected):
    values = _xml_values(_response(context).text, _ctx(context).interpolate_string(xpath))
    expected = _ctx(context).interpolate_string(expected)
    assert values, f"XPath '{xpath}' selected nothing"
    assert values[0] == expected, f"XPath '{xpath}': expected '{expected}', got '{values[0]}'"


def _assert_xml_count(context, xpath, count):
    values = _xml_values(_response(context).text, xpath)
    assert len(values) == count, f"XPath '{xpath}': expected {count} nodes, got {len(values)}"


def _extract_xml(context, xpath, variable):
    values = _xml_values(_response(context).text, xpath)
    assert values, f"XPath '{xpath}' selected nothing"
    _ctx(context).set_variable(variable, values[0])


def _strip(obj, fields):
    if isinstance(obj, dict):
        return {k: _strip(v, fields) for k, v in obj.items() if k not in fields}
    if isinstance(obj, list):
        return [_strip(v, fields) for v in obj]
    return obj


def _assert_json_equals_ignoring(context, fields, expected_text):
    ignore = {f.strip() for f in fields.split(",") if f.strip()}
    expected = json.loads(_ctx(context).interpolate_string(expected_text))
    actual = _response(context).json
    a, e = _strip(actual, ignore), _strip(expected, ignore)
    assert a == e, f"JSON differs (ignoring {sorted(ignore)}):\nexpected: {json.dumps(e, ensure_ascii=False)}\nactual:   {json.dumps(a, ensure_ascii=False)}"


def _soap(context, endpoint, action, body):
    jc = _ctx(context)
    jc.make_request("POST", endpoint, data=jc.interpolate_string(body).encode("utf-8"),
                    headers={"Content-Type": "text/xml; charset=utf-8", "SOAPAction": action})


@step('I set the timeout to {seconds:g} seconds')
def step_set_timeout(context, seconds):
    """Set the HTTP request timeout"""
    _set_timeout(context, seconds)


@step('I disable SSL verification')
def step_disable_ssl(context):
    """Disable TLS certificate verification (testing only)"""
    _disable_ssl(context)


@step('I use the CA bundle "{path}"')
def step_ca_bundle(context, path):
    """Verify TLS using a custom CA bundle file"""
    _use_ca_bundle(context, path)


@step('I use the client certificate "{cert}" and key "{key}"')
def step_client_cert(context, cert, key):
    """Use a client certificate and key (mutual TLS)"""
    _use_client_cert(context, cert, key)


@step('I use the proxy "{url}"')
def step_proxy(context, url):
    """Send requests through an HTTP proxy"""
    _use_proxy(context, url)


@step('I connect to the database "{url}"')
def step_db_connect(context, url):
    """Connect to SQLite, PostgreSQL or MySQL using a URL"""
    _sql_connect(context, url)


@step('I upload the file "{path}" as "{field}" to "{endpoint}"')
def step_upload(context, path, field, endpoint):
    """Upload a file as multipart/form-data with POST"""
    _upload(context, path, field, endpoint)


@step('the response SHA-256 should be "{expected}"')
def step_sha256(context, expected):
    """Validate the SHA-256 digest of the response body"""
    _assert_sha256(context, expected)


@step('the response header "{name}" should be "{value}"')
def step_header_equals(context, name, value):
    """Validate a response header value"""
    _assert_header_equals(context, name, value)


@step('the response header "{name}" should exist')
def step_header_exists(context, name):
    """Validate a response header is present"""
    _assert_header_exists(context, name)


@step('the response should include security headers')
def step_security_headers(context):
    """Validate HSTS, nosniff and clickjacking protection headers"""
    _assert_security_headers(context)


@step('the response XML "{xpath}" should be "{expected}"')
def step_xml_value(context, xpath, expected):
    """Validate the first value selected by an XPath"""
    _assert_xml_value(context, xpath, expected)


@step('the response XML "{xpath}" should select {count:d} nodes')
def step_xml_count(context, xpath, count):
    """Validate how many nodes an XPath selects"""
    _assert_xml_count(context, xpath, count)


@step('I extract the XML "{xpath}" as "{variable}"')
def step_xml_extract(context, xpath, variable):
    """Store the first value selected by an XPath in a variable"""
    _extract_xml(context, xpath, variable)


@step('the response should equal the JSON ignoring "{fields}"')
def step_json_ignoring(context, fields):
    """Compare the response with the JSON in the step text, ignoring volatile fields"""
    _assert_json_equals_ignoring(context, fields, context.text)


@step('I send a SOAP request to "{endpoint}" with action "{action}"')
def step_soap(context, endpoint, action):
    """Send the XML in the step text as a SOAP request"""
    _soap(context, endpoint, action, context.text)


def _assert_status_class(context, family):
    status = _response(context).status
    assert status // 100 == family, f"Expected a {family}xx status, got {status}"


def _assert_status_one_of(context, codes):
    allowed = {int(c) for c in re.split(r"[,\s]+", codes.strip()) if c}
    status = _response(context).status
    assert status in allowed, f"Expected status in {sorted(allowed)}, got {status}"


@step('the response status should be a client error')
def step_client_error(context):
    """Validate the status is 4xx"""
    _assert_status_class(context, 4)


@step('the response status should be a server error')
def step_server_error(context):
    """Validate the status is 5xx"""
    _assert_status_class(context, 5)


@step('the response status should be one of "{codes}"')
def step_status_one_of(context, codes):
    """Validate the status is one of a comma separated list of codes"""
    _assert_status_one_of(context, codes)
