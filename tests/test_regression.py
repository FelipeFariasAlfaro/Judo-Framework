"""
Regression suite: guarantees steps/behaviors from v1.6.10 keep working.

1. Every step pattern that existed in v1.6.10 must still exist (baseline snapshot).
2. A real behave run of legacy EN/ES features against a fixture server must pass.
"""
import json
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
from support.fixture_server import FixtureServer  # noqa: E402

from judo import cli  # noqa: E402
from judo.runner import cli_runner  # noqa: E402
from judo.utils import step_catalog as sc  # noqa: E402

HERE = Path(__file__).parent


def test_all_v1_6_10_steps_still_exist():
    baseline = {tuple(x) for x in json.loads((HERE / "baseline_steps_v1.6.10.json").read_text("utf-8"))}
    current = {(s["lang"], s["pattern"]) for s in sc.load_catalog()}
    missing = sorted(baseline - current)
    assert not missing, f"Steps removed or renamed since v1.6.10: {missing}"


@pytest.fixture()
def project(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert cli.main(["init", "proj"]) == 0
    proj = tmp_path / "proj"
    (proj / "features" / "sample.feature").unlink()
    return proj


@pytest.fixture(scope="module")
def server():
    srv = FixtureServer().start()
    yield srv
    srv.stop()


def _install(proj: Path, server, names):
    for name in names:
        text = (HERE / "regression" / "features" / name).read_text("utf-8").replace("__BASE__", server.url)
        (proj / "features" / name).write_text(text, "utf-8")


def _run(proj: Path):
    res = cli_runner.run_tests(["features"], cwd=str(proj), fmt="json", timeout=300)
    data = cli_runner.load_result(res["result_file"], only_failures=True)
    return res, data


@pytest.mark.parametrize("feature", ["legacy_en.feature", "legacy_es.feature"])
def test_legacy_features_pass(project, server, feature):
    _install(project, server, [feature])
    res, failed = _run(project)
    assert res["summary"] and res["summary"]["scenarios"] > 0, res["output"][-2000:]
    detail = [(f["name"], s["name"], [st for st in s["steps"] if st["status"] != "passed"][:1])
              for f in failed["features"] for s in f["scenarios"]]
    assert res["summary"]["failed"] == 0, json.dumps(detail, indent=1, default=str)[:4000]


@pytest.mark.parametrize("feature", ["new_en.feature", "new_es.feature"])
def test_new_steps_features_pass(project, server, feature):
    import hashlib
    (project / "data").mkdir()
    (project / "data" / "hello.txt").write_text("hello judo")
    sha = hashlib.sha256(b"hello judo").hexdigest()
    text = (HERE / "regression" / "features" / feature).read_text("utf-8")
    (project / "features" / feature).write_text(text.replace("__BASE__", server.url).replace("__SHA__", sha), "utf-8")
    res, failed = _run(project)
    detail = [(s["name"], [st for st in s["steps"] if st["status"] != "passed"][:1])
              for f in failed["features"] for s in f["scenarios"]]
    assert res["summary"] and res["summary"]["scenarios"] > 0, res["output"][-2000:]
    assert res["summary"]["failed"] == 0, json.dumps(detail, indent=1, default=str)[:5000]


def test_timeout_is_enforced(project, server):
    (project / "features" / "t.feature").write_text(f"""Feature: t
  Scenario: slow endpoint with short timeout
    Given I have a Judo API client
    And the base URL is "{server.url}"
    And I set the timeout to 0.3 seconds
    When I send a GET request to "/slow?ms=2000"
    Then the response status should be 200
""")
    res, failed = _run(project)
    assert res["summary"]["failed"] == 1
    err = json.dumps(failed)
    assert "imeout" in err or "timed out" in err


def test_no_state_leaks_between_scenarios(project, server):
    (project / "features" / "leak.feature").write_text(f"""Feature: isolation
  Background:
    Given I have a Judo API client
    And the base URL is "{server.url}"
  Scenario: sets auth and header
    Given I use basic authentication with username "u" and password "p"
    And I set the header "X-Leak" to "1"
    When I send a GET request to "/echo"
    Then the response should contain "headers"
  Scenario: starts clean
    When I send a GET request to "/echo"
    Then the response field "headers.authorization" should match pattern "^$"
""")
    res, failed = _run(project)
    assert res["summary"]["failed"] == 1  # 2nd scenario must see no Authorization header at all


@pytest.mark.parametrize("feature", ["flow_en.feature", "flow_es.feature"])
def test_flow_features_pass(project, server, feature):
    (project / "data").mkdir()
    (project / "data" / "exists.txt").write_text("x")
    text = (HERE / "regression" / "features" / feature).read_text("utf-8")
    (project / "features" / feature).write_text(text.replace("__BASE__", server.url), "utf-8")
    res, failed = _run(project)
    detail = [(s["name"], [st for st in s["steps"] if st["status"] != "passed"][:2])
              for f in failed["features"] for s in f["scenarios"]]
    assert res["summary"] and res["summary"]["scenarios"] > 0, res["output"][-2000:]
    assert res["summary"]["failed"] == 0, json.dumps(detail, indent=1, default=str)[:5000]
    assert res["summary"]["skipped"] == 1  # the explicit "skip the scenario" scenario


XSD = """<?xml version="1.0"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:x="urn:x">
  <xs:element name="root"><xs:complexType><xs:sequence>
    <xs:element name="user" maxOccurs="unbounded"><xs:complexType><xs:sequence>
      <xs:element name="name" type="xs:string"/></xs:sequence>
      <xs:attribute name="id" type="xs:integer"/></xs:complexType></xs:element>
    <xs:any namespace="urn:x" processContents="lax" minOccurs="0"/>
  </xs:sequence></xs:complexType></xs:element>
</xs:schema>"""


@pytest.mark.parametrize("feature", ["protocols_en.feature", "protocols_es.feature"])
def test_protocol_features_pass(project, server, feature):
    pytest.importorskip("lxml")
    (project / "data").mkdir()
    (project / "data" / "users.xsd").write_text(XSD)
    (project / "data" / "envelope.xml").write_text("<Envelope><Body>from file</Body></Envelope>")
    text = (HERE / "regression" / "features" / feature).read_text("utf-8")
    (project / "features" / feature).write_text(text.replace("__BASE__", server.url), "utf-8")
    res, failed = _run(project)
    detail = [(s["name"], [st for st in s["steps"] if st["status"] != "passed"][:2])
              for f in failed["features"] for s in f["scenarios"]]
    assert res["summary"] and res["summary"]["scenarios"] > 0, res["output"][-2000:]
    assert res["summary"]["failed"] == 0, json.dumps(detail, indent=1, default=str)[:6000]


@pytest.mark.parametrize("feature", ["grpc_en.feature", "grpc_es.feature"])
def test_grpc_features_pass(project, feature):
    pytest.importorskip("grpc_reflection")
    from support.grpc_fixture import GrpcFixture
    fx = GrpcFixture().start()
    try:
        text = (HERE / "regression" / "features" / feature).read_text("utf-8")
        (project / "features" / feature).write_text(text.replace("__GRPC__", fx.target), "utf-8")
        res, failed = _run(project)
        detail = [(s["name"], [st for st in s["steps"] if st["status"] != "passed"][:2])
                  for f in failed["features"] for s in f["scenarios"]]
        assert res["summary"] and res["summary"]["scenarios"] > 0, res["output"][-2000:]
        assert res["summary"]["failed"] == 0, json.dumps(detail, indent=1, default=str)[:6000]
    finally:
        fx.stop()
