"""Tests for the v1.7.0 features: interpolation, config, plugins, coverage, diagnose, negative import, retries."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
from support.fixture_server import FixtureServer  # noqa: E402

from judo import cli, config, coverage, diagnose, importers, plugins  # noqa: E402
from judo.runner import cli_runner  # noqa: E402
from judo.utils import step_catalog as sc  # noqa: E402
from judo.utils.feature_validator import validate_feature_text  # noqa: E402
from judo.utils.interpolation import interpolate  # noqa: E402

CATALOG = sc.load_catalog()


# --- interpolation ---------------------------------------------------------
def test_interpolation_both_syntaxes_and_old_dollar_bug():
    v = {"a": "Ana", "n": 5, "user": {"address": {"city": "X"}, "tags": ["t0", "t1"]}, "my-var": "dash"}
    assert interpolate("${a}|{a}|${n}|{n}", v) == "Ana|Ana|5|5"          # '${a}' used to become '$Ana'
    assert interpolate("${user.address.city} ${user.tags[1]}", v) == "X t1"
    assert interpolate("${nope:-dflt} ${nope}", v) == "dflt ${nope}"
    assert interpolate("{my-var}", v) == "dash"                           # legacy odd names still work
    assert interpolate('{"json": "keeps braces", "x": {"y": 1}}', v) == '{"json": "keeps braces", "x": {"y": 1}}'
    assert len(interpolate("${uuid()}", v)) == 36
    assert interpolate("${random_int(5,5)}", v) == "5"


def test_interpolation_strict_mode(monkeypatch):
    with pytest.raises(AssertionError, match="Undefined variable"):
        interpolate("${missing}", {"a": 1}, strict=True)
    monkeypatch.setenv("JUDO_STRICT_VARS", "true")
    with pytest.raises(AssertionError):
        interpolate("${missing}", {})
    monkeypatch.setenv("TOKEN_X", "abc")
    assert interpolate("${env.TOKEN_X}", {}) == "abc"


# --- config ----------------------------------------------------------------
def test_config_validate_resolve_apply():
    cfg = {"default_env": "dev", "timeout": 30, "environments": {
        "dev": {"baseUrl": "http://d"}, "prod": {"baseUrl": "http://p", "timeout": 5}}}
    assert config.validate(cfg) == []
    assert config.resolve(cfg, "prod")["timeout"] == 5
    env = {"JUDO_TIMEOUT": "99"}
    applied = config.apply_to_environment(config.resolve(cfg, "prod"), env)
    assert env["JUDO_BASE_URL"] == "http://p" and env["JUDO_TIMEOUT"] == "99"   # explicit env wins
    assert "JUDO_TIMEOUT" not in applied
    assert any("unknown key" in e for e in config.validate({"bogus": 1}))
    assert any("expected" in e for e in config.validate({"timeout": "x"}))
    assert any("default_env" in e for e in config.validate({"default_env": "z", "environments": {}}))
    with pytest.raises(ValueError):
        config.resolve(cfg, "nope")


def test_run_rejects_invalid_config(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    cli.main(["init", "p"])
    monkeypatch.chdir(tmp_path / "p")
    (tmp_path / "p" / "config" / "judo.yaml").write_text("timeout: banana\n")
    assert cli.main(["run", "features"]) == 2
    assert "Invalid configuration" in capsys.readouterr().err


# --- plugins ---------------------------------------------------------------
def test_plugin_discovery_and_catalog(tmp_path, monkeypatch):
    pkg = tmp_path / "myplug"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("")
    (pkg / "steps.py").write_text("from behave import step\n@step('my plugin step \"{x}\"')\ndef s(context, x):\n    \"\"\"Plugin doc\"\"\"\n")
    dist = tmp_path / "myplug-1.0.dist-info"
    dist.mkdir()
    (dist / "METADATA").write_text("Metadata-Version: 2.1\nName: myplug\nVersion: 1.0\n")
    (dist / "entry_points.txt").write_text("[judo.plugins]\nmyplug = myplug.steps\n")
    monkeypatch.syspath_prepend(str(tmp_path))
    found = plugins.discover()
    assert [p["name"] for p in found] == ["myplug"]
    cat = sc.load_catalog()
    assert any(s["pattern"] == 'my plugin step "{x}"' and s["module"] == "plugin:myplug" for s in cat)
    assert plugins.load_all() == ["myplug"]


# --- coverage & negative import --------------------------------------------
SPEC = {"info": {"title": "T"}, "servers": [{"url": "http://x"}], "paths": {
    "/users": {"get": {"responses": {"200": {}}},
               "post": {"requestBody": {"content": {"application/json": {"schema": {
                   "type": "object", "required": ["name", "age"],
                   "properties": {"name": {"type": "string"}, "age": {"type": "integer"}}}}}},
                   "responses": {"201": {}}}},
    "/users/{id}": {"get": {"parameters": [{"name": "id", "in": "path"}], "responses": {"200": {}}},
                    "delete": {"parameters": [{"name": "id", "in": "path"}], "responses": {"204": {}}}}}}


def test_negative_import_generates_valid_scenarios():
    text = importers.from_openapi(SPEC, negative=True)
    assert "missing required 'name'" in text and "wrong type for 'name'" in text
    assert "empty body" in text and "unknown resource" in text and "@negative" in text
    assert 'status should be one of "400,422"' in text and "999999999" in text
    assert validate_feature_text(text, CATALOG) == []
    assert "negative" not in importers.from_openapi(SPEC)


def test_coverage(tmp_path):
    f = tmp_path / "a.feature"
    f.write_text('''Feature: x
  Scenario: s
    When I send a GET request to "/users"
    And I send a GET request to "/users/${id}?x=1"
    And hago una petición POST a "/users"
''')
    r = coverage.compute(SPEC, [str(tmp_path)])
    assert r["total"] == 4 and r["covered"] == 3
    assert r["missing"] == ["DELETE /users/{id}"] and r["percent"] == 75.0


# --- diagnose --------------------------------------------------------------
def _res(error, status=None):
    ex = {"response": {"status_code": status}} if status else {}
    return {"features": [{"name": "F", "scenarios": [{"name": "S", "status": "failed", "steps": [
        {"step": "Then x", "status": "failed", "error": error, "exchange": ex}]}]}]}


@pytest.mark.parametrize("error,status,cat", [
    ("Undefined step", None, "undefined_step"),
    ("ReadTimeout: HTTPConnectionPool timed out", None, "environment"),
    ("Expected status 200, but got 401", 401, "auth"),
    ("Expected status 200, but got 404", 404, "not_found"),
    ("Expected status 200, but got 503", 503, "api_bug"),
    ("Expected status 201, but got 422", 422, "validation_error"),
    ("JSONPath $.a: expected 1, but got 2", 200, "assertion_mismatch"),
    ("AttributeError: boom", None, "test_bug"),
    ("No such file: data.json", None, "test_data"),
])
def test_diagnose_categories(error, status, cat):
    out = diagnose.explain(_res(error, status))
    assert out["findings"][0]["category"] == cat and out["findings"][0]["suggested_action"]


# --- runner: retries, junit, parallel ---------------------------------------
@pytest.fixture(scope="module")
def server():
    s = FixtureServer().start()
    yield s
    s.stop()


@pytest.fixture()
def project(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    cli.main(["init", "proj"])
    p = tmp_path / "proj"
    (p / "features" / "sample.feature").unlink()
    (p / "config" / "judo.yaml").unlink()
    return p


def test_retries_mark_flaky_and_junit(project, server):
    (project / "features" / "flaky.feature").write_text(f"""Feature: flaky
  Scenario: succeeds on 3rd call
    Given I have a Judo API client
    And the base URL is "{server.url}"
    When I send a GET request to "/flaky"
    Then the response status should be 200
""")
    import urllib.request
    urllib.request.urlopen(server.url + "/reset").read()
    first = cli_runner.run_tests(["features"], cwd=str(project), fmt="json", retries=0)
    assert first["passed"] is False
    urllib.request.urlopen(server.url + "/reset").read()
    res = cli_runner.run_tests(["features"], cwd=str(project), fmt="json", retries=3, junit=True)
    assert res["passed"] is True and res["summary"]["flaky"] == 1 and res["summary"]["failed"] == 0
    assert list((project / "judo_reports" / "junit").glob("*.xml"))


def test_parallel_run_merges_results(project, server):
    for i in range(3):
        (project / "features" / f"p{i}.feature").write_text(f"""Feature: p{i}
  Scenario: ok
    Given I have a Judo API client
    And the base URL is "{server.url}"
    When I send a GET request to "/health"
    Then the response status should be 200
""")
    res = cli_runner.run_tests(["features"], cwd=str(project), fmt="json", parallel=True, workers=3)
    assert res["passed"] and res["summary"]["features"] == 3 and res["summary"]["passed"] == 3


def test_cli_explain_coverage_markdown(project, server, capsys, monkeypatch):
    monkeypatch.chdir(project)
    (project / "features" / "bad.feature").write_text(f"""Feature: bad
  Scenario: s
    Given I have a Judo API client
    And the base URL is "{server.url}"
    When I send a GET request to "/status?code=503"
    Then the response status should be 200
""")
    assert cli.main(["run", "features", "--format", "json"]) == 1
    capsys.readouterr()
    assert cli.main(["explain", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["findings"][0]["category"] == "api_bug"
    spec = project / "spec.json"
    spec.write_text(json.dumps(SPEC))
    assert cli.main(["coverage", str(spec), "features", "--min", "99"]) == 1
    capsys.readouterr()
    assert cli.main(["steps", "--markdown", "--lang", "en"]) == 0
    assert "#### `I poll" in capsys.readouterr().out


def test_mcp_new_tools(project, server, monkeypatch):
    from judo.mcp import tools
    monkeypatch.setenv("JUDO_MCP_WORKDIR", str(project))
    (project / "spec.json").write_text(json.dumps(SPEC))
    assert tools.api_coverage("spec.json")["total"] == 4
    assert "Judo Framework" in tools.guide()
    d = tools.draft_feature("openapi", json.dumps(SPEC), negative=True)
    assert d["issues"] == [] and "@negative" in d["feature"]
    assert "error" in tools.explain_failure() or "findings" in tools.explain_failure()
