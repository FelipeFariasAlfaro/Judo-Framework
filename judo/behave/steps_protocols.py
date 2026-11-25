"""
Steps for services that do not (only) speak JSON (English):
XML/SOAP, forms, plain text, CSV, binary downloads, Server-Sent Events and GraphQL.

All logic lives in ``_*`` helpers reused by ``steps_protocols_es``.
"""
import csv
import io
import json
import os
import re
import threading
import time
import xml.etree.ElementTree as ET

from behave import step

from .steps_extra import _ctx, _response, _xml_values


def _interp(context, value):
    return _ctx(context).interpolate_string(value)


def _jsonpath(data, path):
    try:
        from jsonpath_ng.ext import parse
    except ImportError:  # pragma: no cover
        from jsonpath_ng import parse
    path = path if path.startswith("$") else "$." + path
    return [m.value for m in parse(path).find(data)]


# ---------------------------------------------------------------------------
# XML / SOAP
# ---------------------------------------------------------------------------
def _parse_xml(text):
    try:
        return ET.fromstring(text.encode("utf-8") if isinstance(text, str) else text)
    except ET.ParseError as exc:
        raise AssertionError(f"The response is not valid XML: {exc}")


def _assert_valid_xml(context):
    _parse_xml(_response(context).text)


def _xml_exists(context, xpath, should_exist):
    values = _xml_values(_response(context).text, _interp(context, xpath))
    assert bool(values) == should_exist, \
        f"XPath '{xpath}' {'selected nothing' if should_exist else 'selected ' + str(len(values)) + ' node(s) but should not'}"


def _xml_contains(context, xpath, text):
    values = _xml_values(_response(context).text, _interp(context, xpath))
    text = _interp(context, text)
    assert values, f"XPath '{xpath}' selected nothing"
    assert any(text in v for v in values), f"XPath '{xpath}': none of {values[:5]} contains '{text}'"


def _xml_matches(context, xpath, pattern):
    values = _xml_values(_response(context).text, _interp(context, xpath))
    assert values, f"XPath '{xpath}' selected nothing"
    assert re.search(pattern, values[0]), f"XPath '{xpath}': '{values[0]}' does not match /{pattern}/"


def _xml_xsd(context, path):
    try:
        from lxml import etree
    except ImportError:
        raise AssertionError("XSD validation needs lxml: pip install 'judo-framework[xml]'")
    path = _interp(context, path)
    assert os.path.isfile(path), f"XSD file not found: {path}"
    schema = etree.XMLSchema(etree.parse(path))
    doc = etree.fromstring(_response(context).content)
    assert schema.validate(doc), "XML does not conform to the XSD: " + "; ".join(
        str(e) for e in list(schema.error_log)[:3])


def _local(tag):
    return tag.rsplit("}", 1)[-1]


def _soap_fault(text):
    """(code, message) of a SOAP 1.1/1.2 fault, or None."""
    root = _parse_xml(text)
    for el in root.iter():
        if _local(el.tag) == "Fault":
            code = message = ""
            for child in el.iter():
                name = _local(child.tag)
                if name == "faultcode" or (name == "Value" and not code):
                    code = (child.text or "").strip()
                elif name == "faultstring" or (name == "Text" and not message):
                    message = (child.text or "").strip()
            return code, message
    return None


def _soap_no_fault(context):
    fault = _soap_fault(_response(context).text)
    assert fault is None, f"SOAP fault received: {fault[0]} - {fault[1]}"


def _soap_fault_code(context, code):
    fault = _soap_fault(_response(context).text)
    assert fault is not None, "The response is not a SOAP fault"
    expected = _interp(context, code)
    assert fault[0] == expected or fault[0].endswith(":" + expected), f"Fault code: expected '{expected}', got '{fault[0]}'"


def _soap_fault_message(context, text):
    fault = _soap_fault(_response(context).text)
    assert fault is not None, "The response is not a SOAP fault"
    assert _interp(context, text) in fault[1], f"Fault message '{fault[1]}' does not contain '{text}'"


def _soap12(context, endpoint, action, body):
    jc = _ctx(context)
    jc.make_request("POST", endpoint, data=jc.interpolate_string(body).encode("utf-8"),
                    headers={"Content-Type": f'application/soap+xml; charset=utf-8; action="{action}"'})


def _soap_from_file(context, endpoint, action, path):
    path = _interp(context, path)
    assert os.path.isfile(path), f"File not found: {path}"
    with open(path, "r", encoding="utf-8") as fh:
        body = fh.read()
    jc = _ctx(context)
    jc.make_request("POST", endpoint, data=jc.interpolate_string(body).encode("utf-8"),
                    headers={"Content-Type": "text/xml; charset=utf-8", "SOAPAction": action})


def _xml_post(context, endpoint, body):
    jc = _ctx(context)
    jc.make_request("POST", endpoint, data=jc.interpolate_string(body).encode("utf-8"),
                    headers={"Content-Type": "application/xml; charset=utf-8"})


# ---------------------------------------------------------------------------
# Forms, text, CSV, binary
# ---------------------------------------------------------------------------
def _form_post(context, endpoint, table):
    assert table is not None, "This step needs a table with the columns: field | value"
    data = {row["field"]: _interp(context, row["value"]) for row in table}
    _ctx(context).make_request("POST", endpoint, data=data,
                               headers={"Content-Type": "application/x-www-form-urlencoded"})


def _form_set(context, name, value):
    if not hasattr(context, "_judo_form_fields"):
        context._judo_form_fields = {}
    context._judo_form_fields[name] = _interp(context, value)


def _form_submit(context, endpoint):
    data = getattr(context, "_judo_form_fields", None)
    assert data, "No form fields set. Use 'I set the form field ...' first."
    _ctx(context).make_request("POST", endpoint, data=dict(data),
                               headers={"Content-Type": "application/x-www-form-urlencoded"})
    context._judo_form_fields = {}


def _text_contains(context, text, negate=False):
    text = _interp(context, text)
    present = text in (_response(context).text or "")
    assert present != negate, f"Response text {'contains' if present else 'does not contain'} '{text}'"


def _text_matches(context, pattern):
    assert re.search(pattern, _response(context).text or "", re.DOTALL), f"Response text does not match /{pattern}/"


def _text_equals(context, text):
    expected = _interp(context, text)
    actual = (_response(context).text or "").strip()
    assert actual == expected.strip(), f"Expected text '{expected}', got '{actual[:200]}'"


def _content_type(context, expected):
    actual = next((v for k, v in _response(context).headers.items() if k.lower() == "content-type"), "")
    assert actual.lower().startswith(expected.lower()), f"Content-Type: expected '{expected}', got '{actual}'"


def _size_less(context, size):
    actual = len(_response(context).content)
    assert actual < size, f"Response size {actual} bytes is not less than {size}"


def _csv_rows(context):
    return list(csv.DictReader(io.StringIO(_response(context).text or "")))


def _csv_count(context, count):
    rows = _csv_rows(context)
    assert len(rows) == count, f"Expected {count} CSV rows, got {len(rows)}"


def _csv_column(context, column, value):
    rows = _csv_rows(context)
    assert rows and column in rows[0], f"CSV column '{column}' not found. Columns: {list(rows[0]) if rows else []}"
    value = _interp(context, value)
    assert any(r[column] == value for r in rows), f"CSV column '{column}' has no value '{value}'"


def _bytes_equal_file(context, path):
    path = _interp(context, path)
    assert os.path.isfile(path), f"File not found: {path}"
    with open(path, "rb") as fh:
        expected = fh.read()
    assert _response(context).content == expected, "Response bytes differ from the file content"


def _download(context, endpoint, path):
    jc = _ctx(context)
    jc.make_request("GET", endpoint)
    assert jc.response.status < 400, f"Download failed with status {jc.response.status}"
    path = _interp(context, path)
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(jc.response.content)


def _download_name(context, name):
    disp = next((v for k, v in _response(context).headers.items() if k.lower() == "content-disposition"), "")
    m = re.search(r'filename\*?=(?:UTF-8\'\')?"?([^";]+)"?', disp)
    assert m, f"No filename in Content-Disposition: '{disp}'"
    assert m.group(1) == _interp(context, name), f"Download filename: expected '{name}', got '{m.group(1)}'"


def _save_text(context, variable):
    _ctx(context).set_variable(variable, _response(context).text)


# ---------------------------------------------------------------------------
# Server-Sent Events
# ---------------------------------------------------------------------------
class _SSEStream:
    def __init__(self, url, headers):
        import requests
        self.events = []
        self.closed = False
        self.finished = False
        self.error = None
        self._cond = threading.Condition()
        self._resp = requests.get(url, headers=headers, stream=True, timeout=(10, 60))
        self.status = self._resp.status_code
        self._thread = threading.Thread(target=self._read, daemon=True)
        self._thread.start()

    def _read(self):
        event, data, eid = "message", [], None
        try:
            for raw in self._resp.iter_lines(decode_unicode=True):
                if self.closed:
                    break
                if raw is None:
                    continue
                if raw == "":
                    if data:
                        with self._cond:
                            self.events.append({"event": event, "data": "\n".join(data), "id": eid})
                            self._cond.notify_all()
                    event, data = "message", []
                elif raw.startswith(":"):
                    continue
                else:
                    field, _, value = raw.partition(":")
                    value = value[1:] if value.startswith(" ") else value
                    if field == "event":
                        event = value
                    elif field == "data":
                        data.append(value)
                    elif field == "id":
                        eid = value
        except Exception as exc:  # connection closed by close() or server
            if not self.closed:
                self.error = exc
        finally:
            with self._cond:
                self.finished = True
                self._cond.notify_all()

    def wait(self, predicate, seconds):
        deadline = time.time() + seconds
        with self._cond:
            while True:
                hit = predicate(self.events)
                if hit:
                    return hit
                left = deadline - time.time()
                if left <= 0:
                    return None
                self._cond.wait(left)

    def close(self):
        self.closed = True
        try:
            self._resp.close()
        except Exception:
            pass


def _sse_open(context, endpoint):
    jc = _ctx(context)
    client = jc.judo.http_client
    headers = {k: v for k, v in client.default_headers.items() if k.lower() not in ("content-type", "accept")}
    headers["Accept"] = "text/event-stream"
    old = getattr(context, "_judo_sse", None)
    if old:
        old.close()
    stream = _SSEStream(client._build_url(jc.interpolate_string(endpoint)), headers)
    assert stream.status < 400, f"SSE connection failed with status {stream.status}"
    context._judo_sse = stream
    if hasattr(context, "add_cleanup"):
        context.add_cleanup(stream.close)


def _sse(context):
    stream = getattr(context, "_judo_sse", None)
    assert stream is not None, "No SSE stream open. Use 'I open the SSE stream \"...\"' first."
    return stream


def _sse_event(context, name, seconds):
    name = _interp(context, name)
    hit = _sse(context).wait(lambda evs: next((e for e in evs if e["event"] == name), None), seconds)
    assert hit, f"No SSE event '{name}' within {seconds}s. Received: {[e['event'] for e in _sse(context).events]}"


def _sse_data_contains(context, text, seconds):
    text = _interp(context, text)
    hit = _sse(context).wait(lambda evs: next((e for e in evs if text in e["data"]), None), seconds)
    assert hit, f"No SSE event with data containing '{text}' within {seconds}s"


def _sse_count(context, count, seconds):
    hit = _sse(context).wait(lambda evs: len(evs) >= count or None, seconds)
    assert hit, f"Expected {count} SSE events within {seconds}s, got {len(_sse(context).events)}"


def _sse_last(context, path, expected):
    events = _sse(context).events
    assert events, "No SSE events received yet"
    data = json.loads(events[-1]["data"])
    found = _jsonpath(data, path)
    expected = _interp(context, expected)
    assert found and str(found[0]) == str(expected), f"SSE data '{path}': expected '{expected}', got {found[:1]}"


def _sse_close(context):
    stream = getattr(context, "_judo_sse", None)
    if stream:
        stream.close()
        context._judo_sse = None


# ---------------------------------------------------------------------------
# GraphQL
# ---------------------------------------------------------------------------
def _gql_vars(context, text):
    try:
        context._judo_gql_vars = json.loads(_interp(context, text))
    except ValueError as exc:
        raise AssertionError(f"GraphQL variables are not valid JSON: {exc}")


def _gql_send(context, endpoint, query):
    payload = {"query": _interp(context, query)}
    variables = getattr(context, "_judo_gql_vars", None)
    if variables:
        payload["variables"] = variables
    _ctx(context).make_request("POST", endpoint, json=payload)
    context._judo_gql_vars = None


def _gql_body(context):
    body = _response(context).json
    assert isinstance(body, dict), "The GraphQL response is not a JSON object"
    return body


def _gql_no_errors(context):
    errors = _gql_body(context).get("errors")
    assert not errors, "GraphQL errors: " + "; ".join(str(e.get("message", e)) for e in errors[:3])


def _gql_error_contains(context, text):
    errors = _gql_body(context).get("errors") or []
    text = _interp(context, text)
    assert any(text in str(e.get("message", e)) for e in errors), f"No GraphQL error contains '{text}'. Errors: {errors}"


def _gql_data(context, path):
    return _jsonpath(_gql_body(context).get("data") or {}, path)


def _gql_data_equals(context, path, expected):
    found = _gql_data(context, path)
    expected = _interp(context, expected)
    assert found and str(found[0]) == str(expected), f"GraphQL data '{path}': expected '{expected}', got {found[:1]}"


def _gql_data_exists(context, path):
    assert _gql_data(context, path), f"GraphQL data '{path}' not found"


def _gql_data_count(context, path, count):
    found = _gql_data(context, path)
    assert found and isinstance(found[0], list) and len(found[0]) == count, \
        f"GraphQL data '{path}': expected {count} items, got {len(found[0]) if found and isinstance(found[0], list) else found[:1]}"


def _gql_save(context, path, variable):
    found = _gql_data(context, path)
    assert found, f"GraphQL data '{path}' not found"
    _ctx(context).set_variable(variable, found[0])


_INTROSPECTION = "query IntrospectionQuery { __schema { types { name kind } } }"


def _gql_introspect(context, endpoint):
    _ctx(context).make_request("POST", endpoint, json={"query": _INTROSPECTION})
    _gql_no_errors(context)


def _gql_type(context, name):
    types = _gql_data(context, "__schema.types")
    names = [t.get("name") for t in (types[0] if types else [])]
    assert _interp(context, name) in names, f"GraphQL type '{name}' not found. Types: {names[:15]}"


# ---------------------------------------------------------------------------
# English steps: XML / SOAP
# ---------------------------------------------------------------------------
@step('the response should be valid XML')
def step_valid_xml(context):
    """Validate the response body is well-formed XML"""
    _assert_valid_xml(context)


@step('the response XML "{xpath}" should exist')
def step_xml_exists(context, xpath):
    """Validate an XPath selects at least one node"""
    _xml_exists(context, xpath, True)


@step('the response XML "{xpath}" should not exist')
def step_xml_not_exists(context, xpath):
    """Validate an XPath selects nothing"""
    _xml_exists(context, xpath, False)


@step('the response XML "{xpath}" should contain "{text}"')
def step_xml_contains(context, xpath, text):
    """Validate a node selected by an XPath contains a text"""
    _xml_contains(context, xpath, text)


@step('the response XML "{xpath}" should match "{pattern}"')
def step_xml_matches(context, xpath, pattern):
    """Validate the first node selected by an XPath matches a regex"""
    _xml_matches(context, xpath, pattern)


@step('the response XML should conform to the XSD "{path}"')
def step_xml_xsd(context, path):
    """Validate the response XML against an XSD schema (needs lxml)"""
    _xml_xsd(context, path)


@step('the SOAP response should not be a fault')
def step_soap_no_fault(context):
    """Validate the SOAP response is not a fault"""
    _soap_no_fault(context)


@step('the SOAP fault code should be "{code}"')
def step_soap_fault_code(context, code):
    """Validate the SOAP fault code"""
    _soap_fault_code(context, code)


@step('the SOAP fault message should contain "{text}"')
def step_soap_fault_message(context, text):
    """Validate the SOAP fault message contains a text"""
    _soap_fault_message(context, text)


@step('I send a SOAP 1.2 request to "{endpoint}" with action "{action}"')
def step_soap12(context, endpoint, action):
    """Send the XML in the step text as a SOAP 1.2 request"""
    _soap12(context, endpoint, action, context.text)


@step('I send the SOAP envelope file "{path}" to "{endpoint}" with action "{action}"')
def step_soap_file(context, path, endpoint, action):
    """Send a SOAP 1.1 request whose envelope is read from a file"""
    _soap_from_file(context, endpoint, action, path)


@step('I send an XML POST to "{endpoint}"')
def step_xml_post(context, endpoint):
    """POST the XML in the step text with Content-Type application/xml"""
    _xml_post(context, endpoint, context.text)


# ---------------------------------------------------------------------------
# English steps: forms, text, CSV, binary
# ---------------------------------------------------------------------------
@step('I send a form POST to "{endpoint}"')
def step_form_post(context, endpoint):
    """POST application/x-www-form-urlencoded using a table with columns field | value"""
    _form_post(context, endpoint, context.table)


@step('I set the form field "{name}" to "{value}"')
def step_form_set(context, name, value):
    """Stage a form field for the next 'I submit the form'"""
    _form_set(context, name, value)


@step('I submit the form to "{endpoint}"')
def step_form_submit(context, endpoint):
    """POST the staged form fields as application/x-www-form-urlencoded"""
    _form_submit(context, endpoint)


@step('the response text should contain "{text}"')
def step_text_contains(context, text):
    """Validate the response text contains a string"""
    _text_contains(context, text)


@step('the response text should not contain "{text}"')
def step_text_not_contains(context, text):
    """Validate the response text does not contain a string"""
    _text_contains(context, text, negate=True)


@step('the response text should match "{pattern}"')
def step_text_matches(context, pattern):
    """Validate the response text matches a regular expression"""
    _text_matches(context, pattern)


@step('the response text should equal "{text}"')
def step_text_equals(context, text):
    """Validate the whole response text (trimmed)"""
    _text_equals(context, text)


@step('the response content type should be "{content_type}"')
def step_content_type(context, content_type):
    """Validate the Content-Type header starts with a value"""
    _content_type(context, content_type)


@step('the response size should be less than {size:d} bytes')
def step_size_less(context, size):
    """Validate the response body size"""
    _size_less(context, size)


@step('the response should be a CSV with {count:d} rows')
def step_csv_count(context, count):
    """Validate the number of CSV data rows (header excluded)"""
    _csv_count(context, count)


@step('the CSV column "{column}" should contain "{value}"')
def step_csv_column(context, column, value):
    """Validate a CSV column has a value in some row"""
    _csv_column(context, column, value)


@step('the response bytes should equal the file "{path}"')
def step_bytes_equal(context, path):
    """Validate the response bytes are identical to a file"""
    _bytes_equal_file(context, path)


@step('I download "{endpoint}" to the file "{path}"')
def step_download(context, endpoint, path):
    """GET an endpoint and save the raw bytes to a file"""
    _download(context, endpoint, path)


@step('the response should have the download filename "{name}"')
def step_download_name(context, name):
    """Validate the filename in Content-Disposition"""
    _download_name(context, name)


@step('I save the response text as "{variable}"')
def step_save_text(context, variable):
    """Store the raw response text in a variable"""
    _save_text(context, variable)


# ---------------------------------------------------------------------------
# English steps: SSE
# ---------------------------------------------------------------------------
@step('I open the SSE stream "{endpoint}"')
def step_sse_open(context, endpoint):
    """Open a Server-Sent Events stream and collect events in the background"""
    _sse_open(context, endpoint)


@step('I should receive an SSE event "{event}" within {seconds:g} seconds')
def step_sse_event(context, event, seconds):
    """Wait for an SSE event by name"""
    _sse_event(context, event, seconds)


@step('I should receive an SSE event with data containing "{text}" within {seconds:g} seconds')
def step_sse_data(context, text, seconds):
    """Wait for an SSE event whose data contains a text"""
    _sse_data_contains(context, text, seconds)


@step('I should receive {count:d} SSE events within {seconds:g} seconds')
def step_sse_count(context, count, seconds):
    """Wait until at least N SSE events have arrived"""
    _sse_count(context, count, seconds)


@step('the last SSE event data "{json_path}" should be "{expected}"')
def step_sse_last(context, json_path, expected):
    """Validate a JSON field of the last SSE event data"""
    _sse_last(context, json_path, expected)


@step('I close the SSE stream')
def step_sse_close(context):
    """Close the SSE stream"""
    _sse_close(context)


# ---------------------------------------------------------------------------
# English steps: GraphQL
# ---------------------------------------------------------------------------
@step('I set the GraphQL variables')
def step_gql_vars(context):
    """Set the variables (JSON in the step text) for the next GraphQL request"""
    _gql_vars(context, context.text)


@step('I send the GraphQL query to "{endpoint}"')
def step_gql_query(context, endpoint):
    """Send the GraphQL query in the step text"""
    _gql_send(context, endpoint, context.text)


@step('I send the GraphQL mutation to "{endpoint}"')
def step_gql_mutation(context, endpoint):
    """Send the GraphQL mutation in the step text"""
    _gql_send(context, endpoint, context.text)


@step('the GraphQL response should not have errors')
def step_gql_no_errors(context):
    """Validate the GraphQL response has no errors"""
    _gql_no_errors(context)


@step('the GraphQL response should have an error containing "{text}"')
def step_gql_error(context, text):
    """Validate a GraphQL error message contains a text"""
    _gql_error_contains(context, text)


@step('the GraphQL data "{json_path}" should be "{expected}"')
def step_gql_data_equals(context, json_path, expected):
    """Validate a value inside the GraphQL data"""
    _gql_data_equals(context, json_path, expected)


@step('the GraphQL data "{json_path}" should exist')
def step_gql_data_exists(context, json_path):
    """Validate a path exists inside the GraphQL data"""
    _gql_data_exists(context, json_path)


@step('the GraphQL data "{json_path}" should have {count:d} items')
def step_gql_data_count(context, json_path, count):
    """Validate the size of an array inside the GraphQL data"""
    _gql_data_count(context, json_path, count)


@step('I save the GraphQL data "{json_path}" as "{variable}"')
def step_gql_save(context, json_path, variable):
    """Store a value of the GraphQL data in a variable"""
    _gql_save(context, json_path, variable)


@step('I introspect the GraphQL schema at "{endpoint}"')
def step_gql_introspect(context, endpoint):
    """Run the introspection query"""
    _gql_introspect(context, endpoint)


@step('the GraphQL schema should have the type "{name}"')
def step_gql_type(context, name):
    """Validate a type exists in the introspected schema"""
    _gql_type(context, name)
