"""
gRPC steps (English). Uses server reflection, so no .proto files are required.
Install the optional dependencies with: pip install "judo-framework[grpc]"
"""
import json

from behave import step

from .steps_extra import _ctx

_MISSING = object()


def _client(context):
    client = getattr(context, "_judo_grpc", None)
    assert client is not None, "Not connected. Use 'I connect to the gRPC server \"host:port\"' first."
    return client


def _interp(context, value):
    return _ctx(context).interpolate_string(value)


def _jsonpath(data, path):
    try:
        from jsonpath_ng.ext import parse
    except ImportError:  # pragma: no cover
        from jsonpath_ng import parse
    path = path if path.startswith("$") else "$." + path
    return [m.value for m in parse(path).find(data)]


def _connect(context, target, tls=False):
    from ..features.grpc_client import GrpcClient
    old = getattr(context, "_judo_grpc", None)
    if old:
        old.close()
    context._judo_grpc = GrpcClient(_interp(context, target), tls=tls,
                                    timeout=getattr(context, "_judo_grpc_timeout", 10.0))
    context._judo_grpc_last = None
    context._judo_grpc_stream = None
    if hasattr(context, "add_cleanup"):
        context.add_cleanup(context._judo_grpc.close)


def _set_timeout(context, seconds):
    context._judo_grpc_timeout = float(seconds)
    if getattr(context, "_judo_grpc", None):
        context._judo_grpc.timeout = float(seconds)


def _set_metadata(context, key, value):
    _client(context).metadata.append((key.lower(), _interp(context, value)))


def _send(context, method, body):
    client = _client(context)
    context._judo_grpc_last = client.call(_interp(context, method), _interp(context, body or "{}"))
    context._judo_grpc_stream = None


def _send_stream(context, method, body):
    client = _client(context)
    context._judo_grpc_stream = client.stream(_interp(context, method), _interp(context, body or "{}"))
    context._judo_grpc_last = None


def _assert_status(context, status):
    actual = _client(context).last_status
    details = _client(context).last_details
    assert actual == status.upper(), f"gRPC status: expected {status.upper()}, got {actual}" + (f" ({details})" if details else "")


def _last(context):
    last = getattr(context, "_judo_grpc_last", None)
    assert last is not None, f"No gRPC response (status {_client(context).last_status}: {_client(context).last_details})"
    return last


def _assert_value(context, path, expected):
    found = _jsonpath(_last(context), path)
    expected = _interp(context, expected)
    assert found and str(found[0]) == str(expected), f"gRPC response '{path}': expected '{expected}', got {found[:1]}"


def _assert_contains(context, field):
    assert _jsonpath(_last(context), field), f"gRPC response has no field '{field}'. Response: {json.dumps(_last(context))[:300]}"


def _save(context, path, variable):
    found = _jsonpath(_last(context), path)
    assert found, f"gRPC response has no '{path}'"
    _ctx(context).set_variable(variable, found[0])


def _assert_service(context, service):
    services = _client(context).list_services()
    assert _interp(context, service) in services, f"Service '{service}' not exposed. Available: {services}"


def _assert_method(context, method):
    assert _client(context).has_method(_interp(context, method)), f"Method '{method}' not exposed by the server"


def _stream(context):
    msgs = getattr(context, "_judo_grpc_stream", None)
    assert msgs is not None, "No gRPC stream. Use 'I send the gRPC streaming request ...' first."
    return msgs


def _assert_stream_count(context, count):
    n = len(_stream(context))
    assert n == count, f"Expected {count} stream messages, got {n}"


def _assert_stream_value(context, index, path, expected):
    msgs = _stream(context)
    assert 0 <= index < len(msgs), f"Stream has {len(msgs)} messages, index {index} is out of range"
    found = _jsonpath(msgs[index], path)
    expected = _interp(context, expected)
    assert found and str(found[0]) == str(expected), f"Stream message {index} '{path}': expected '{expected}', got {found[:1]}"


def _assert_time(context, ms):
    actual = _client(context).last_elapsed_ms
    assert actual < ms, f"gRPC call took {actual} ms (limit {ms} ms)"


def _close(context):
    client = getattr(context, "_judo_grpc", None)
    if client:
        client.close()
        context._judo_grpc = None


@step('I connect to the gRPC server "{target}"')
def step_grpc_connect(context, target):
    """Open an insecure gRPC channel (host:port)"""
    _connect(context, target)


@step('I connect to the gRPC server "{target}" with TLS')
def step_grpc_connect_tls(context, target):
    """Open a TLS gRPC channel using the system trust store"""
    _connect(context, target, tls=True)


@step('I set the gRPC metadata "{key}" to "{value}"')
def step_grpc_metadata(context, key, value):
    """Add a metadata (header) sent with every gRPC call"""
    _set_metadata(context, key, value)


@step('I set the gRPC timeout to {seconds:g} seconds')
def step_grpc_timeout(context, seconds):
    """Set the deadline of gRPC calls"""
    _set_timeout(context, seconds)


@step('I send the gRPC request "{method}"')
def step_grpc_send(context, method):
    """Call a unary method; the request (JSON) goes in the step text"""
    _send(context, method, context.text)


@step('I send the gRPC streaming request "{method}"')
def step_grpc_send_stream(context, method):
    """Call a server-streaming method; the request (JSON) goes in the step text"""
    _send_stream(context, method, context.text)


@step('the gRPC status should be "{status}"')
def step_grpc_status(context, status):
    """Validate the gRPC status code name (OK, NOT_FOUND, UNAUTHENTICATED, ...)"""
    _assert_status(context, status)


@step('the gRPC response "{json_path}" should be "{expected}"')
def step_grpc_value(context, json_path, expected):
    """Validate a field of the gRPC response"""
    _assert_value(context, json_path, expected)


@step('the gRPC response should contain "{field}"')
def step_grpc_contains(context, field):
    """Validate the gRPC response has a field"""
    _assert_contains(context, field)


@step('I save the gRPC response "{json_path}" as "{variable}"')
def step_grpc_save(context, json_path, variable):
    """Store a field of the gRPC response in a variable"""
    _save(context, json_path, variable)


@step('the gRPC server should expose the service "{service}"')
def step_grpc_service(context, service):
    """Validate (via reflection) that a service is exposed"""
    _assert_service(context, service)


@step('the gRPC server should expose the method "{method}"')
def step_grpc_method(context, method):
    """Validate (via reflection) that a method exists"""
    _assert_method(context, method)


@step('the gRPC stream should return {count:d} messages')
def step_grpc_stream_count(context, count):
    """Validate how many messages the server stream returned"""
    _assert_stream_count(context, count)


@step('the gRPC stream message {index:d} "{json_path}" should be "{expected}"')
def step_grpc_stream_value(context, index, json_path, expected):
    """Validate a field of one stream message (0-based index)"""
    _assert_stream_value(context, index, json_path, expected)


@step('the gRPC call should take less than {ms:d} milliseconds')
def step_grpc_time(context, ms):
    """Validate the duration of the last gRPC call"""
    _assert_time(context, ms)


@step('I close the gRPC connection')
def step_grpc_close(context):
    """Close the gRPC channel"""
    _close(context)
