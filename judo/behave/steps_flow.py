"""
Conditional and control-flow steps (English).

Behave has no ``if``, so a condition step receives the steps to run as a docstring block
and executes them with ``context.execute_steps``::

    When I send a GET request to "/users/1"
    And if the response status is 404 then run
      \"\"\"
      When I send a POST request to "/users" with JSON
        '''
        {"name": "Ana"}
        '''
      \"\"\"
    And otherwise run
      \"\"\"
      Then the response "$.active" should be "True"
      \"\"\"

Use ``'''`` for a docstring nested inside a block. The logic lives in ``_*`` helpers that the
Spanish module (``steps_flow_es``) reuses.
"""
import os
import re
import time

from behave import step

from .steps_extra import _ctx

_FIRST_KEYWORD = re.compile(r"^\s*(And|But|Y|Pero|E|\*)\s+", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Block execution
# ---------------------------------------------------------------------------
def _normalize_block(text):
    """Dedent, convert nested ''' docstrings to \"\"\", and make a leading And/But usable."""
    lines = [l.rstrip() for l in (text or "").splitlines()]
    while lines and not lines[0].strip():
        lines.pop(0)
    out = []
    for i, line in enumerate(lines):
        line = line.replace("'''", '"""')
        if i == 0:
            line = _FIRST_KEYWORD.sub("* ", line)
        out.append(line)
    return "\n".join(out)


def _run_block(context, text):
    assert text and text.strip(), "This step needs a block of steps in a docstring (\"\"\" ... \"\"\")"
    context.execute_steps(_normalize_block(text))


def _if(context, ok, block):
    context._judo_last_condition = bool(ok)
    if ok:
        _run_block(context, block)


def _otherwise(context, block):
    assert hasattr(context, "_judo_last_condition"), "'otherwise run' needs a previous 'if ... then run' step"
    if not context._judo_last_condition:
        _run_block(context, block)
    context._judo_last_condition = True  # an else is consumed once


# ---------------------------------------------------------------------------
# Condition evaluation
# ---------------------------------------------------------------------------
def _response(context):
    resp = _ctx(context).response
    assert resp is not None, "No response available. Make a request first."
    return resp


def _json_find(context, path):
    """Return the list of values matched by a JSONPath expression ([] when none)."""
    try:
        from jsonpath_ng.ext import parse
    except ImportError:  # pragma: no cover
        from jsonpath_ng import parse
    body = _response(context).json
    return [m.value for m in parse(_ctx(context).interpolate_string(path)).find(body)]


def _first(context, path):
    found = _json_find(context, path)
    return found[0] if found else None


def _status_is(context, status):
    return _response(context).status == status


def _json_equals(context, path, expected):
    found = _json_find(context, path)
    expected = _ctx(context).interpolate_string(expected)
    return bool(found) and str(found[0]) == str(expected)


def _json_exists(context, path):
    return bool(_json_find(context, path))


def _json_contains(context, path, text):
    found = _json_find(context, path)
    text = _ctx(context).interpolate_string(text)
    if not found:
        return False
    value = found[0]
    if isinstance(value, (list, tuple)):
        return any(str(v) == text or text in str(v) for v in value)
    return text in str(value)


def _json_number(context, path, number, greater):
    value = _first(context, path)
    try:
        value = float(value)
    except (TypeError, ValueError):
        return False
    return value > number if greater else value < number


def _var_defined(context, name):
    return _ctx(context).get_variable(name, None) is not None


def _var_equals(context, name, expected):
    jc = _ctx(context)
    value = jc.get_variable(name, None)
    return value is not None and str(value) == str(jc.interpolate_string(expected))


def _var_empty(context, name):
    value = _ctx(context).get_variable(name, None)
    return value is None or value == "" or value == [] or value == {}


def _env_name():
    return os.getenv("JUDO_ENV") or os.getenv("KARATE_ENV") or ""


def _env_is(env):
    return _env_name() == env


def _envvar_set(name):
    return bool(os.getenv(name))


def _has_tag(context, tag):
    scenario = getattr(context, "scenario", None)
    tags = {str(t) for t in getattr(scenario, "effective_tags", getattr(scenario, "tags", [])) or []}
    return tag.lstrip("@") in tags


def _file_exists(context, path):
    return os.path.exists(_ctx(context).interpolate_string(path))


def _header_exists(context, name):
    return any(k.lower() == name.lower() for k in _response(context).headers)


def _body_contains(context, text):
    return _ctx(context).interpolate_string(text) in (_response(context).text or "")


def _time_over(context, ms):
    elapsed = getattr(_response(context), "elapsed", 0) or 0
    return elapsed * 1000 > ms


# ---------------------------------------------------------------------------
# Skip / fail / assertions about state
# ---------------------------------------------------------------------------
def _skip(context, reason):
    context.scenario.skip(reason)


def _fail(context, message):
    raise AssertionError(_ctx(context).interpolate_string(message))


def _assert_defined(context, name, expected_defined):
    defined = _var_defined(context, name)
    assert defined == expected_defined, f"Variable '{name}' should {'be' if expected_defined else 'not be'} defined"


def _assert_empty(context, name):
    assert _var_empty(context, name), f"Variable '{name}' should be empty, got {_ctx(context).get_variable(name)!r}"


def _assert_env(env):
    assert _env_is(env), f"Expected environment '{env}', running in '{_env_name() or '(not set)'}'"


# ---------------------------------------------------------------------------
# Loops, retry, soft assertions
# ---------------------------------------------------------------------------
def _repeat(context, count, block):
    jc = _ctx(context)
    for i in range(1, count + 1):
        jc.set_variable("iteration", i)
        _run_block(context, block)


def _repeat_until(context, path, expected, count, block):
    jc = _ctx(context)
    for i in range(1, count + 1):
        jc.set_variable("iteration", i)
        _run_block(context, block)
        if _json_equals(context, path, expected):
            return
    raise AssertionError(f'"{path}" never became "{expected}" after {count} iterations')


def _for_each(context, path, block):
    jc = _ctx(context)
    items = _first(context, path)
    assert isinstance(items, list), f'"{path}" is not an array (got {type(items).__name__})'
    for index, item in enumerate(items):
        jc.set_variable("item", item)
        jc.set_variable("index", index)
        _run_block(context, block)


def _retry(context, count, seconds, block):
    last = None
    for attempt in range(1, count + 1):
        try:
            _run_block(context, block)
            return
        except AssertionError as exc:
            last = exc
            if attempt < count:
                time.sleep(seconds)
    raise AssertionError(f"Block still failing after {count} attempts. Last error: {last}")


def _soft(context, block):
    failures = []
    for line in _normalize_block(block).splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        try:
            context.execute_steps(_FIRST_KEYWORD.sub("* ", line.strip()))
        except AssertionError as exc:
            failures.append(f"{line.strip()}\n    -> {str(exc).splitlines()[0] if str(exc) else 'failed'}")
    assert not failures, f"{len(failures)} soft assertion(s) failed:\n  " + "\n  ".join(failures)


# ---------------------------------------------------------------------------
# English steps: conditions (block in the docstring)
# ---------------------------------------------------------------------------
@step('if the response status is {status:d} then run')
def step_if_status(context, status):
    """Run the docstring steps when the response status matches"""
    _if(context, _status_is(context, status), context.text)


@step('if the response status is not {status:d} then run')
def step_if_status_not(context, status):
    """Run the docstring steps when the response status differs"""
    _if(context, not _status_is(context, status), context.text)


@step('if the response "{json_path}" equals "{expected}" then run')
def step_if_json_equals(context, json_path, expected):
    """Run the docstring steps when a JSON path equals a value"""
    _if(context, _json_equals(context, json_path, expected), context.text)


@step('if the response "{json_path}" exists then run')
def step_if_json_exists(context, json_path):
    """Run the docstring steps when a JSON path exists"""
    _if(context, _json_exists(context, json_path), context.text)


@step('if the response "{json_path}" does not exist then run')
def step_if_json_missing(context, json_path):
    """Run the docstring steps when a JSON path does not exist"""
    _if(context, not _json_exists(context, json_path), context.text)


@step('if the response "{json_path}" contains "{text}" then run')
def step_if_json_contains(context, json_path, text):
    """Run the docstring steps when a JSON value (or array item) contains the text"""
    _if(context, _json_contains(context, json_path, text), context.text)


@step('if the response "{json_path}" is greater than {number:g} then run')
def step_if_json_gt(context, json_path, number):
    """Run the docstring steps when a numeric JSON value is greater than a number"""
    _if(context, _json_number(context, json_path, number, True), context.text)


@step('if the response "{json_path}" is less than {number:g} then run')
def step_if_json_lt(context, json_path, number):
    """Run the docstring steps when a numeric JSON value is less than a number"""
    _if(context, _json_number(context, json_path, number, False), context.text)


@step('if the variable "{name}" equals "{expected}" then run')
def step_if_var_equals(context, name, expected):
    """Run the docstring steps when a variable equals a value"""
    _if(context, _var_equals(context, name, expected), context.text)


@step('if the variable "{name}" is defined then run')
def step_if_var_defined(context, name):
    """Run the docstring steps when a variable is defined"""
    _if(context, _var_defined(context, name), context.text)


@step('if the variable "{name}" is not defined then run')
def step_if_var_undefined(context, name):
    """Run the docstring steps when a variable is not defined"""
    _if(context, not _var_defined(context, name), context.text)


@step('if the variable "{name}" is empty then run')
def step_if_var_empty(context, name):
    """Run the docstring steps when a variable is missing or empty"""
    _if(context, _var_empty(context, name), context.text)


@step('if the environment is "{env}" then run')
def step_if_env(context, env):
    """Run the docstring steps when JUDO_ENV / KARATE_ENV equals the value"""
    _if(context, _env_is(env), context.text)


@step('if the environment variable "{name}" is set then run')
def step_if_envvar(context, name):
    """Run the docstring steps when an OS environment variable is set"""
    _if(context, _envvar_set(name), context.text)


@step('if the scenario has the tag "{tag}" then run')
def step_if_tag(context, tag):
    """Run the docstring steps when the scenario carries a tag"""
    _if(context, _has_tag(context, tag), context.text)


@step('if the file "{path}" exists then run')
def step_if_file(context, path):
    """Run the docstring steps when a file exists"""
    _if(context, _file_exists(context, path), context.text)


@step('if the response header "{name}" exists then run')
def step_if_header(context, name):
    """Run the docstring steps when a response header is present"""
    _if(context, _header_exists(context, name), context.text)


@step('if the response body contains "{text}" then run')
def step_if_body(context, text):
    """Run the docstring steps when the raw response body contains the text"""
    _if(context, _body_contains(context, text), context.text)


@step('if the response time is greater than {ms:d} milliseconds then run')
def step_if_slow(context, ms):
    """Run the docstring steps when the response was slower than the limit"""
    _if(context, _time_over(context, ms), context.text)


@step('otherwise run')
def step_otherwise(context):
    """Run the docstring steps when the previous 'if' condition was false"""
    _otherwise(context, context.text)


# ---------------------------------------------------------------------------
# English steps: skip, fail, state assertions
# ---------------------------------------------------------------------------
@step('I skip the scenario if the variable "{name}" equals "{expected}"')
def step_skip_var(context, name, expected):
    """Skip the rest of the scenario when a variable equals a value"""
    if _var_equals(context, name, expected):
        _skip(context, f'variable "{name}" equals "{expected}"')


@step('I skip the scenario if the environment is "{env}"')
def step_skip_env(context, env):
    """Skip the rest of the scenario in a given environment"""
    if _env_is(env):
        _skip(context, f'environment is "{env}"')


@step('I skip the scenario if the response status is {status:d}')
def step_skip_status(context, status):
    """Skip the rest of the scenario when the response status matches"""
    if _status_is(context, status):
        _skip(context, f"response status is {status}")


@step('I fail the test with the message "{message}"')
def step_fail(context, message):
    """Fail the scenario with a custom message"""
    _fail(context, message)


@step('the variable "{name}" should be defined')
def step_var_defined(context, name):
    """Validate a variable is defined"""
    _assert_defined(context, name, True)


@step('the variable "{name}" should not be defined')
def step_var_not_defined(context, name):
    """Validate a variable is not defined"""
    _assert_defined(context, name, False)


@step('the variable "{name}" should be empty')
def step_var_empty(context, name):
    """Validate a variable is missing or empty"""
    _assert_empty(context, name)


@step('the environment should be "{env}"')
def step_env_should(context, env):
    """Validate the current environment name"""
    _assert_env(env)


# ---------------------------------------------------------------------------
# English steps: loops, retry, soft assertions
# ---------------------------------------------------------------------------
@step('I repeat {count:d} times')
def step_repeat(context, count):
    """Run the docstring steps N times (variable ${iteration} = 1..N)"""
    _repeat(context, count, context.text)


@step('I repeat until the response "{json_path}" equals "{expected}" up to {count:d} times')
def step_repeat_until(context, json_path, expected, count):
    """Run the docstring steps until a JSON path equals a value, at most N times"""
    _repeat_until(context, json_path, expected, count, context.text)


@step('for each item in the response "{json_path}" run')
def step_for_each(context, json_path):
    """Run the docstring steps for each array element (variables ${item} and ${index})"""
    _for_each(context, json_path, context.text)


@step('I retry the following steps up to {count:d} times with {seconds:g} seconds delay')
def step_retry(context, count, seconds):
    """Retry the docstring steps while they fail"""
    _retry(context, count, seconds, context.text)


@step('I verify all of the following')
def step_soft(context):
    """Run each docstring line as a step and report every failure at the end"""
    _soft(context, context.text)
