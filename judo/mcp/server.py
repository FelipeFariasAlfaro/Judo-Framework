"""
Judo MCP server (stdio). Start with ``judo mcp``.

Requires the optional dependency: ``pip install judo-framework[mcp]``.
"""
from typing import Any, Dict, List, Optional

from . import tools


def build_server():
    try:  # mcp >= 2
        from mcp.server.mcpserver import MCPServer as FastMCP
    except ImportError:
        try:  # mcp 1.x
            from mcp.server.fastmcp import FastMCP
        except ImportError as exc:  # pragma: no cover
            raise SystemExit("The MCP server needs the 'mcp' package: pip install 'judo-framework[mcp]'") from exc

    mcp = FastMCP("judo", instructions=(
        "Judo Framework API testing. Always call search_steps before writing a step by hand, "
        "validate_feature before run_tests, and never put secrets in features."))

    @mcp.tool()
    def search_steps(query: str, lang: Optional[str] = None, category: Optional[str] = None,
                     limit: int = 15) -> Dict:
        """Find Judo steps by text. lang: 'en' or 'es'. Returns exact patterns to use in .feature files."""
        return tools.search_steps(query, lang, category, limit)

    @mcp.tool()
    def list_step_categories() -> Dict:
        """List step categories with counts, and step totals per language."""
        return tools.list_step_categories()

    @mcp.tool()
    def get_step(pattern: str) -> Dict:
        """Details of one step by its exact pattern (module, line, params, description)."""
        return tools.get_step(pattern)

    @mcp.tool()
    def draft_feature(source_type: str, content: str, tag_filter: Optional[str] = None,
                      negative: bool = False) -> Dict:
        """Generate a .feature draft from a curl command, an OpenAPI spec or a Postman collection.
        source_type: 'curl' | 'openapi' | 'postman'. content: raw text (JSON/YAML for specs).
        negative=true (openapi) also generates missing/wrong-field and unknown-id cases."""
        return tools.draft_feature(source_type, content, tag_filter, negative)

    @mcp.tool()
    def validate_feature(path: Optional[str] = None, text: Optional[str] = None) -> Dict:
        """Check a feature file/folder (path) or raw feature text for undefined or ambiguous steps."""
        return tools.validate_feature(path, text)

    @mcp.tool()
    def write_feature(path: str, content: str, overwrite: bool = False) -> Dict:
        """Save a .feature file inside the working directory (validates it and reports issues)."""
        return tools.write_feature(path, content, overwrite)

    @mcp.tool()
    def run_tests(path: str = "features", tags: Optional[List[str]] = None, env: Optional[str] = None,
                  rerun_failed: bool = False, fail_fast: bool = False, parallel: bool = False,
                  dry_run: bool = False) -> Dict:
        """Run tests and return a compact summary plus failing scenarios with masked request/response."""
        return tools.run_tests(path, tags, env, rerun_failed, fail_fast, parallel, dry_run)

    @mcp.tool()
    def explain_failure() -> Dict:
        """Classify the failures of the last run (undefined step, environment, auth, not found, API bug,
        validation, assertion mismatch, test data, test bug) with evidence and a suggested next action."""
        return tools.explain_failure()

    @mcp.tool()
    def api_coverage(spec_path: str, features_path: str = "features") -> Dict:
        """Percentage of OpenAPI operations exercised by the features, and the ones not covered."""
        return tools.api_coverage(spec_path, features_path)

    @mcp.resource("judo://guide")
    def guide_resource() -> str:
        """How to write and run Judo tests (rules, commands, minimal feature)."""
        return tools.guide()

    @mcp.resource("judo://steps")
    def steps_resource() -> str:
        """The full step catalog as JSON (pattern, language, category, description)."""
        import json as _json
        from ..utils import step_catalog as _sc
        return _json.dumps(_sc.public_catalog(tools._catalog()), ensure_ascii=False)

    @mcp.prompt()
    def generate_tests_from_openapi(spec_path: str, tag: str = "") -> str:
        """Plan for creating a complete test suite from an OpenAPI file."""
        return (f"Create Judo tests for the API described in '{spec_path}'" + (f" (tag: {tag})" if tag else "") + ".\n"
                "1. Call draft_feature(source_type='openapi', content=<spec text>, negative=true).\n"
                "2. Replace placeholder data with realistic values; keep secrets as ${VARIABLES}.\n"
                "3. validate_feature on the draft and fix every undefined step using search_steps.\n"
                "4. write_feature under features/, then run_tests and api_coverage.\n"
                "5. If something fails, call explain_failure before changing the tests.")

    @mcp.prompt()
    def triage_failure() -> str:
        """Step by step triage of the last failed run."""
        return ("Call explain_failure. For each finding: if category is api_bug or environment, do NOT edit the test; "
                "report it with the evidence. If assertion_mismatch, compare with get_last_report(only_failures=true) "
                "and decide whether the API changed or the test is stale. If undefined_step/test_bug, fix the feature "
                "using search_steps and validate_feature, then re-run only the failures with run_tests(rerun_failed=true).")

    @mcp.tool()
    def get_last_report(only_failures: bool = False) -> Dict:
        """Read the last JSON results (judo_reports/result.json)."""
        return tools.get_last_report(only_failures)

    @mcp.tool()
    def list_reports() -> Dict:
        """List recent report files."""
        return tools.list_reports()

    @mcp.tool()
    def send_request(method: str, url: str, headers: Optional[Dict[str, str]] = None,
                     body: Optional[Any] = None, timeout: int = 30) -> Dict:
        """Send one HTTP request to explore an API. Limited to JUDO_MCP_ALLOWED_HOSTS. Secrets masked."""
        return tools.send_request(method, url, headers, body, timeout)

    @mcp.tool()
    def get_env() -> Dict:
        """Judo-related environment variables (secrets masked) and working directory."""
        return tools.get_env()

    @mcp.tool()
    def start_mock(port: int = 8089, routes: Optional[List[Dict]] = None) -> Dict:
        """Start a mock server. routes: [{method, path, status, body}]."""
        return tools.start_mock(port, routes)

    @mcp.tool()
    def stop_mock(port: int = 8089) -> Dict:
        """Stop a mock server started with start_mock."""
        return tools.stop_mock(port)

    return mcp


def main():
    build_server().run()


if __name__ == "__main__":
    main()
