"""
Command Line Interface for Judo Framework

Commands: run, init, mock, steps, validate, import, mcp, doctor, version
"""
import argparse
import json
import os
import sys
from pathlib import Path
from typing import List, Optional


def _print_json(data) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False, default=str))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Judo Framework - API Testing Framework for Python', prog='judo')
    sub = parser.add_subparsers(dest='command', help='Available commands')

    run = sub.add_parser('run', help='Run feature files')
    run.add_argument('paths', nargs='*', help='Feature files or folders (default: features)')
    run.add_argument('--tags', '-t', action='append', help='Behave tag expression (repeatable), e.g. smoke or ~wip')
    run.add_argument('--env', '-e', help='Environment name (sets KARATE_ENV / JUDO_ENV)')
    run.add_argument('--parallel', '-p', action='store_true', help='Run one process per feature file')
    run.add_argument('--workers', '-w', type=int, default=4, help='Parallel workers (default 4)')
    run.add_argument('--fail-fast', action='store_true', help='Stop at the first failure')
    run.add_argument('--rerun-failed', action='store_true', help='Only rerun scenarios that failed last time')
    run.add_argument('--format', dest='fmt', choices=['pretty', 'json'], default='pretty',
                     help="'json' prints a compact JSON result (AI/CI friendly)")
    run.add_argument('--dry-run', action='store_true', help='Parse and match steps without executing')
    run.add_argument('--retries', type=int, default=0, help='Retry failed scenarios N times (reports flaky ones)')
    run.add_argument('--junit', action='store_true', help='Also write JUnit XML to judo_reports/junit')
    run.add_argument('--config', help='Path to judo.yaml (default: config/judo.yaml or judo.yaml)')
    run.add_argument('--verbose', '-v', action='store_true')

    init = sub.add_parser('init', help='Create a new Judo (behave) project')
    init.add_argument('name', help='Project name / folder')
    init.add_argument('--ai', choices=['kiro', 'cursor', 'claude', 'generic', 'all'],
                      help='Also generate AI assistant instructions and MCP config')

    mock = sub.add_parser('mock', help='Start a mock server')
    mock.add_argument('--port', '-p', type=int, default=8080)
    mock.add_argument('--config', '-c', help='JSON/YAML file: {"routes":[{"method","path","status","body"}]}')

    steps = sub.add_parser('steps', help='List and search available steps')
    steps.add_argument('--search', '-s', help='Text to search for')
    steps.add_argument('--lang', choices=['en', 'es'])
    steps.add_argument('--category', '-c')
    steps.add_argument('--json', action='store_true', dest='as_json')
    steps.add_argument('--markdown', action='store_true', help='Print the step reference as Markdown')
    steps.add_argument('--check', action='store_true',
                       help='Fail if there are duplicated patterns or EN/ES steps are out of sync')

    val = sub.add_parser('validate', help='Detect undefined/ambiguous steps without running tests')
    val.add_argument('paths', nargs='*', default=['features'])
    val.add_argument('--json', action='store_true', dest='as_json')

    imp = sub.add_parser('import', help='Generate a .feature draft from curl, OpenAPI or Postman')
    imp.add_argument('kind', choices=['curl', 'openapi', 'postman'])
    imp.add_argument('source', help='File path (for curl, a file containing the command or the command text)')
    imp.add_argument('--output', '-o', help='Output .feature file (default: stdout)')
    imp.add_argument('--tag', help='OpenAPI: only operations with this tag')
    imp.add_argument('--negative', action='store_true',
                     help='OpenAPI: also generate negative cases (missing/wrong fields, unknown ids)')

    cov = sub.add_parser('coverage', help='Which OpenAPI operations do the features exercise?')
    cov.add_argument('spec', help='OpenAPI file (json/yaml)')
    cov.add_argument('paths', nargs='*', default=['features'])
    cov.add_argument('--json', action='store_true', dest='as_json')
    cov.add_argument('--min', type=float, default=None, help='Fail if coverage %% is below this value')

    exp = sub.add_parser('explain', help='Classify the failures of the last run (cause + suggested action)')
    exp.add_argument('--result', default='judo_reports/result.json')
    exp.add_argument('--json', action='store_true', dest='as_json')

    sub.add_parser('mcp', help='Start the MCP server (stdio). Needs: pip install "judo-framework[mcp]"')
    sub.add_parser('doctor', help='Check the environment')
    sub.add_parser('version', help='Show version')
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    handlers = {
        'run': cmd_run, 'init': cmd_init, 'mock': cmd_mock, 'steps': cmd_steps,
        'validate': cmd_validate, 'import': cmd_import, 'mcp': cmd_mcp,
        'doctor': cmd_doctor, 'version': lambda a: show_version(),
        'coverage': cmd_coverage, 'explain': cmd_explain,
    }
    if args.command not in handlers:
        parser.print_help()
        return 0
    code = handlers[args.command](args)
    return code or 0


# ---------------------------------------------------------------------------
def cmd_run(args) -> int:
    from judo.runner.cli_runner import run_tests, load_result
    from judo import config as jconfig
    cfg_path = Path(args.config) if args.config else jconfig.find_config()
    cfg_values = {}
    if cfg_path and cfg_path.exists():
        cfg = jconfig.load(cfg_path)
        errors = jconfig.validate(cfg)
        if errors:
            print(f"Invalid configuration {cfg_path}:\n  " + "\n  ".join(errors), file=sys.stderr)
            return 2
        try:
            cfg_values = jconfig.resolve(cfg, args.env)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 2
        jconfig.apply_to_environment(cfg_values)
    retries = args.retries or int(cfg_values.get('retries', 0) or 0)
    res = run_tests(args.paths or None, tags=args.tags, env=args.env, parallel=args.parallel,
                    workers=args.workers, fail_fast=args.fail_fast, rerun_failed=args.rerun_failed,
                    fmt=args.fmt, dry_run=args.dry_run, verbose=args.verbose, stream=args.fmt == 'pretty',
                    junit=args.junit, retries=retries)
    if args.fmt == 'json':
        data = load_result(res['result_file'], compact=True) if Path(res['result_file']).exists() else {}
        data['returncode'] = res['returncode']
        if not data.get('summary'):
            data['output'] = res['output'][-3000:]
        _print_json(data)
    elif args.parallel:
        print(res['output'])
    return res['returncode']


def cmd_steps(args) -> int:
    from judo.utils import step_catalog as sc
    catalog = sc.load_catalog()
    if args.markdown:
        print(steps_markdown(catalog, args.lang))
        return 0
    if args.check:
        problems = [f"Duplicate: {d['pattern']} ({', '.join(d['locations'])})" for d in sc.find_duplicates(catalog)]
        en = sum(1 for s in catalog if s['lang'] == 'en' and 'genai' not in s['module'])
        es = sum(1 for s in catalog if s['lang'] == 'es' and 'genai' not in s['module'])
        print(f"EN steps: {en} | ES steps: {es}")
        for p in problems:
            print(p)
        return 1 if problems else 0
    if args.search:
        items = sc.search_steps(args.search, catalog, args.lang, args.category, limit=25)
    else:
        items = [s for s in sc.public_catalog(catalog)
                 if (not args.lang or s['lang'] == args.lang) and (not args.category or s['category'] == args.category)]
    if args.as_json:
        _print_json({"count": len(items), "steps": items})
    else:
        for s in items:
            print(f"[{s['lang']}] {s['pattern']}" + (f"  - {s['description']}" if s['description'] else ""))
        print(f"\n{len(items)} steps")
    return 0


def cmd_validate(args) -> int:
    from judo.utils.feature_validator import validate_paths
    result = validate_paths(args.paths)
    if args.as_json:
        _print_json(result)
    else:
        for i in result['issues']:
            tag = 'ERROR' if i['severity'] == 'error' else 'WARN '
            print(f"{tag} {i['file']}:{i['line']}  {i['step']}")
            if i.get('suggestions'):
                print("      did you mean: " + " | ".join(i['suggestions']))
            if i.get('matches'):
                print("      matches: " + " | ".join(i['matches']))
        print(f"\n{result['files']} files, {result['errors']} errors, {result['warnings']} warnings")
    return 0 if result['ok'] else 1


def cmd_import(args) -> int:
    from judo import importers
    if args.kind == 'curl' and not os.path.exists(args.source):
        text = importers.from_curl(args.source)
    else:
        text = importers.from_file(args.kind, args.source, args.tag, args.negative)
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(text, encoding='utf-8')
        print(f"Feature written to {args.output}")
    else:
        print(text)
    return 0


def steps_markdown(catalog, lang=None) -> str:
    from collections import defaultdict
    groups = defaultdict(list)
    for s in catalog:
        if lang and s['lang'] != lang:
            continue
        groups[s['category']].append(s)
    out = ["# Judo steps reference", "", "_Generated from the code with `judo steps --markdown`._", ""]
    for cat in sorted(groups):
        out += [f"## {cat}", ""]
        for s in sorted(groups[cat], key=lambda x: x['pattern']):
            out.append(f"#### `{s['pattern']}` ({s['lang']})")
            if s['description']:
                out.append(s['description'] + ".")
        out.append("")
    return "\n".join(out)


def cmd_coverage(args) -> int:
    from judo import coverage
    result = coverage.compute(coverage.load_spec(args.spec), args.paths)
    if args.as_json:
        _print_json(result)
    else:
        print(f"API coverage: {result['covered']}/{result['total']} operations ({result['percent']}%)")
        for m in result['missing']:
            print(f"  not covered: {m}")
    if args.min is not None and result['percent'] < args.min:
        return 1
    return 0


def cmd_explain(args) -> int:
    from judo import diagnose
    p = Path(args.result)
    if not p.exists():
        print(f"{p} not found. Run `judo run --format json` first.", file=sys.stderr)
        return 2
    report = diagnose.explain(json.loads(p.read_text(encoding='utf-8')))
    if args.as_json:
        _print_json(report)
    else:
        print(f"{report['failed_scenarios']} failed scenarios: {report['by_category']}")
        for f in report['findings']:
            print(f"\n[{f['category']}] {f['feature']} / {f['scenario']}\n  step: {f['step']}")
            for e in f['evidence'][:3]:
                print(f"  evidence: {e}")
            print(f"  next: {f['suggested_action']}")
    return 0


def cmd_mcp(args) -> int:
    from judo.mcp.server import main as mcp_main
    mcp_main()
    return 0


def cmd_doctor(args) -> int:
    import importlib
    import platform
    from judo import __version__
    print(f"Judo {__version__} | Python {platform.python_version()}")
    required = ['behave', 'requests', 'jsonpath_ng', 'yaml', 'jsonschema', 'jinja2', 'dotenv']
    optional = {'mcp': 'mcp', 'openai': 'genai', 'anthropic': 'genai', 'lxml': 'xml', 'openpyxl': 'excel'}
    bad = 0
    for mod in required:
        try:
            importlib.import_module(mod)
            print(f"  ok       {mod}")
        except ImportError:
            print(f"  MISSING  {mod}")
            bad += 1
    for mod, extra in optional.items():
        try:
            importlib.import_module(mod)
            print(f"  ok       {mod} (optional)")
        except ImportError:
            print(f"  absent   {mod} (optional: pip install 'judo-framework[{extra}]')")
    from judo import config as jconfig, plugins
    cfg_path = jconfig.find_config()
    if cfg_path:
        errs = jconfig.validate(jconfig.load(cfg_path))
        print(f"  config    {cfg_path} " + ("ok" if not errs else "INVALID"))
        for e in errs:
            print(f"            - {e}")
        bad += 1 if errs else 0
    for p in plugins.discover():
        print(f"  plugin    {p['name']} ({p['module']})")
    root = Path.cwd()
    print(f"  features/ {'found' if (root / 'features').is_dir() else 'not found in ' + str(root)}")
    print(f"  .env      {'found' if (root / '.env').exists() else 'not found'}")
    return 1 if bad else 0


# ---------------------------------------------------------------------------
_ENV_PY = '''"""Behave environment: Judo hooks (reporting, context)."""
from judo.behave import *

before_all = before_all_judo
before_feature = before_feature_judo
after_feature = after_feature_judo
before_scenario = before_scenario_judo
after_scenario = after_scenario_judo
before_step = before_step_judo
after_step = after_step_judo
after_all = after_all_judo
'''

_STEPS_PY = '''"""Judo steps (English + Spanish). Add your own custom steps below."""
from judo.behave import *  # noqa: F401,F403
'''

_SAMPLE = '''@smoke
Feature: Sample API test

  Background:
    Given I have a Judo API client
    And the base URL is "https://jsonplaceholder.typicode.com"

  Scenario: Get a post
    When I send a GET request to "/posts/1"
    Then the response status should be 200
    And the response "$.userId" should be 1
'''

_CONFIG = '''# Judo Framework configuration (validated by `judo doctor` and `judo run`)
default_env: dev
timeout: 30          # seconds per request
verify_ssl: true
retries: 0           # retry failed scenarios N times
environments:
  dev:
    baseUrl: "https://api-dev.example.com"
  test:
    baseUrl: "https://api-test.example.com"
  prod:
    baseUrl: "https://api.example.com"
    timeout: 15
'''


def cmd_init(args) -> int:
    name = args.name
    root = Path(name)
    (root / 'features' / 'steps').mkdir(parents=True, exist_ok=True)
    (root / 'config').mkdir(exist_ok=True)
    files = {
        root / 'features' / 'environment.py': _ENV_PY,
        root / 'features' / 'steps' / 'judo_steps.py': _STEPS_PY,
        root / 'features' / 'sample.feature': _SAMPLE,
        root / 'config' / 'judo.yaml': _CONFIG,
        root / '.env': '# JUDO_BASE_URL=https://api.example.com\n# TOKEN=\n',
        root / '.gitignore': '.env\njudo_reports/\nrerun_failing.features\n__pycache__/\n',
    }
    if args.ai:
        from judo.ai_templates import files_for, MCP_CONFIG
        for rel, content in files_for(args.ai).items():
            files[root / rel] = content
        if args.ai in ('kiro', 'all'):
            files[root / '.kiro' / 'settings' / 'mcp.json'] = json.dumps(MCP_CONFIG, indent=2) + '\n'
        if args.ai in ('cursor', 'all'):
            files[root / '.cursor' / 'mcp.json'] = json.dumps(MCP_CONFIG, indent=2) + '\n'
        if args.ai in ('claude', 'all'):
            files[root / '.mcp.json'] = json.dumps(MCP_CONFIG, indent=2) + '\n'
    for path, content in files.items():
        if path.exists():
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
    print(f"Project '{name}' created.")
    print(f"  cd {name} && judo run features/")
    return 0


def cmd_mock(args) -> int:
    from judo.mock.server import MockServer
    server = MockServer(args.port)
    if args.config:
        raw = Path(args.config).read_text(encoding='utf-8')
        if args.config.endswith(('.yaml', '.yml')):
            import yaml
            cfg = yaml.safe_load(raw)
        else:
            cfg = json.loads(raw)
        for r in cfg.get('routes', []):
            server.add_route(r.get('method', 'GET'), r['path'],
                             {"status": r.get('status', 200), "body": r.get('body', {})})
        print(f"Loaded {len(cfg.get('routes', []))} routes from {args.config}")
    else:
        server.get("/health", {"status": 200, "body": {"status": "ok"}})
        server.get("/users/*", {"status": 200, "body": {"id": 1, "name": "John Doe"}})
    try:
        server.start()
        print(f"Mock server on http://localhost:{args.port}. Ctrl+C to stop.")
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop()
        print("\nMock server stopped.")
    return 0


def show_version() -> int:
    from judo import __version__
    print(f"Judo Framework v{__version__}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
