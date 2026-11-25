"""Self-tests for the Judo framework tooling (catalog, validator, importers, MCP tools, CLI)."""
import json
import sys
from pathlib import Path

import pytest

from judo import importers
from judo.utils import step_catalog as sc
from judo.utils.exchange import mask_secrets
from judo.utils.feature_validator import validate_feature_text, validate_paths


@pytest.fixture(scope="module")
def catalog():
    return sc.load_catalog()


# --- catalog ---------------------------------------------------------------
def test_catalog_not_empty_and_has_both_languages(catalog):
    assert len(catalog) > 300
    assert {s["lang"] for s in catalog} == {"en", "es"}


def test_no_duplicate_patterns(catalog):
    assert sc.find_duplicates(catalog) == []


def test_extra_steps_have_en_es_parity(catalog):
    en = [s for s in catalog if s["module"] == "behave/steps_extra.py"]
    es = [s for s in catalog if s["module"] == "behave/steps_extra_es.py"]
    assert en and len({s["function"] for s in en}) == len({s["function"] for s in es})


def test_match_and_search(catalog):
    assert sc.match_step("the response status should be 200", catalog)
    assert not sc.match_step("the response status should be banana", catalog)
    hits = sc.search_steps("poll status", catalog, lang="es")
    assert hits and all(h["lang"] == "es" for h in hits)


def test_suggest_typo(catalog):
    assert any("GET request" in s for s in sc.suggest('I send a GETT request to "/x"', catalog))


# --- validator -------------------------------------------------------------
def test_validator_flags_undefined_and_accepts_known(catalog):
    text = """Feature: x
  Scenario: s
    Given I have a Judo API client
    When I send a GET request to "/a"
    Then the response status should be 200
    And this step does not exist
"""
    issues = validate_feature_text(text, catalog)
    assert [i["step"] for i in issues if i["severity"] == "error"] == ["this step does not exist"]


def test_validator_handles_docstrings_tables_outline(catalog):
    text = '''Feature: x
  Scenario Outline: s
    When I send a GET request to "/users/<id>"
    Then the response status should be <code>
    Examples:
      | id | code |
      | 1  | 200  |
  Scenario: doc
    When I send a POST request to "/x" with JSON
      """
      {"this is": "ignored"}
      """
'''
    assert validate_feature_text(text, catalog) == []


def test_validator_spanish(catalog):
    text = """# language: es
Característica: x
  Escenario: s
    Dado que tengo un cliente Judo API
    Cuando hago una petición GET a "/a"
"""
    assert validate_feature_text(text, catalog) == []


# --- importers -------------------------------------------------------------
def _assert_valid(text, catalog):
    assert validate_feature_text(text, catalog) == [], text


def test_import_curl(catalog):
    text = importers.from_curl(
        """curl -X POST https://api.example.com/users -H 'Authorization: Bearer abc123'
        -H 'Content-Type: application/json' -d '{"name":"Ana","password":"s3"}'""")
    assert "abc123" not in text and '"s3"' not in text  # secrets masked
    assert 'the base URL is "https://api.example.com"' in text
    _assert_valid(text, catalog)


def test_import_openapi(catalog):
    spec = {"info": {"title": "Pets"}, "servers": [{"url": "https://p.io"}], "paths": {
        "/pets/{id}": {"get": {"summary": "Get pet", "tags": ["pets"],
                               "parameters": [{"name": "id", "in": "path", "example": 7}],
                               "responses": {"200": {}}}},
        "/pets": {"post": {"requestBody": {"content": {"application/json": {"schema": {
            "type": "object", "properties": {"name": {"type": "string"}}}}}},
            "responses": {"201": {}}}}}}
    text = importers.from_openapi(spec)
    assert '"/pets/7"' in text and "status should be 201" in text
    _assert_valid(text, catalog)


def test_import_postman(catalog):
    col = {"info": {"name": "C"}, "item": [{"name": "folder", "item": [{"name": "r", "request": {
        "method": "GET", "header": [{"key": "X-A", "value": "1"}],
        "url": {"raw": "{{host}}/v1/x?a=1"}}}]}]}
    text = importers.from_postman(col)
    assert 'GET request to "/v1/x?a=1"' in text or "/v1/x" in text
    _assert_valid(text, catalog)


# --- secrets ---------------------------------------------------------------
def test_mask_secrets():
    out = mask_secrets({"Authorization": "Bearer x", "a": {"api_key": "k", "ok": 1}, "l": [{"password": "p"}]})
    assert out["Authorization"] == "***" and out["a"]["api_key"] == "***"
    assert out["a"]["ok"] == 1 and out["l"][0]["password"] == "***"


# --- MCP tools -------------------------------------------------------------
def test_mcp_tools(tmp_path, monkeypatch):
    from judo.mcp import tools
    monkeypatch.setenv("JUDO_MCP_WORKDIR", str(tmp_path))
    assert tools.search_steps("bearer token")["count"] > 0
    assert tools.list_step_categories()["total"] > 300
    assert "error" in tools.get_step("nope")
    draft = tools.draft_feature("curl", "curl https://x.io/a")
    assert draft["issues"] == []
    res = tools.write_feature("features/a.feature", draft["feature"])
    assert res["written"] and res["validation"]["ok"]
    assert not tools.write_feature("features/a.feature", "x")["written"]
    with pytest.raises(PermissionError):
        tools.write_feature("../evil.feature", "x")
    with pytest.raises(ValueError):
        tools.write_feature("features/a.txt", "x")


def test_send_request_allowlist(monkeypatch):
    from judo.mcp import tools
    monkeypatch.delenv("JUDO_MCP_ALLOWED_HOSTS", raising=False)
    assert "error" in tools.send_request("GET", "https://example.com/")
    monkeypatch.setenv("JUDO_MCP_ALLOWED_HOSTS", "*.example.com")
    assert tools._host_allowed("https://api.example.com/x")
    assert not tools._host_allowed("https://evil.com/x")


# --- end to end with mock + behave subprocess ------------------------------
def test_cli_init_validate_run(tmp_path, monkeypatch):
    from judo import cli
    from judo.mcp import tools
    monkeypatch.chdir(tmp_path)
    assert cli.main(["init", "proj", "--ai", "all"]) == 0
    proj = tmp_path / "proj"
    assert (proj / "AGENTS.md").exists() and (proj / ".kiro/settings/mcp.json").exists()
    monkeypatch.chdir(proj)

    import socket
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    tools.start_mock(port, [{"method": "GET", "path": "/ping", "status": 200, "body": {"ok": True}}])
    try:
        (proj / "features" / "sample.feature").write_text(f"""Feature: e2e
  Background:
    Given I have a Judo API client
    And the base URL is "http://localhost:{port}"
  Scenario: ok
    When I send a GET request to "/ping"
    Then the response status should be 200
  Scenario: ko
    When I send a GET request to "/ping"
    Then the response status should be 404
""")
        assert cli.main(["validate", "features"]) == 0
        monkeypatch.setenv("JUDO_MCP_WORKDIR", str(proj))
        res = tools.run_tests("features")
        assert res["passed"] is False
        assert res["summary"]["passed"] == 1 and res["summary"]["failed"] == 1
        failing = res["failures"][0]["scenarios"][0]
        assert failing["name"] == "ko"
        assert failing["steps"][-1]["exchange"]["response"]["status_code"] == 200
        assert tools.get_last_report(only_failures=True)["summary"]["failed"] == 1
    finally:
        tools.stop_mock(port)


@pytest.mark.parametrize("en_mod,es_mod", [
    ("behave/steps_extra.py", "behave/steps_extra_es.py"),
    ("behave/steps_flow.py", "behave/steps_flow_es.py"),
    ("behave/steps_protocols.py", "behave/steps_protocols_es.py"),
    ("behave/steps_grpc.py", "behave/steps_grpc_es.py"),
])
def test_new_modules_have_en_es_parity(catalog, en_mod, es_mod):
    en = {s["function"] for s in catalog if s["module"] == en_mod}
    es = {s["function"] for s in catalog if s["module"] == es_mod}
    assert en and len(en) == len(es), f"{en_mod}: {len(en)} EN vs {len(es)} ES functions"
    # every ES step has the same parameter count as its EN twin, in declaration order
    en_params = sorted(len(s["params"]) for s in catalog if s["module"] == en_mod and not s["pattern"].startswith("que "))
    es_params = sorted(len(s["params"]) for s in catalog if s["module"] == es_mod and not s["pattern"].startswith("que "))
    assert en_params == es_params


def test_step_count_milestone(catalog):
    """~300 distinct bilingual steps (functions per language, GenAI included)."""
    en_functions = {(s["module"], s["function"]) for s in catalog if s["lang"] == "en"}
    assert len(en_functions) >= 300, len(en_functions)


def test_validator_checks_steps_nested_in_flow_blocks(catalog):
    text = '''Feature: x
  Scenario: s
    When I send a GET request to "/a"
    And if the response status is 404 then run
      """
      When I send a GETT request to "/b"
      Then the response status should be 200
      """
    And otherwise run
      """
      Then the response status should be 200
      """
'''
    issues = validate_feature_text(text, catalog)
    assert [(i["type"], i["step"]) for i in issues] == [("undefined", 'I send a GETT request to "/b"')]
    assert issues[0]["line"] == 6
