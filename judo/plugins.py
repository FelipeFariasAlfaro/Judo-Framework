"""
Plugin loader. Third-party packages add steps/features by declaring an entry point:

    [project.entry-points."judo.plugins"]
    my_plugin = "my_package.judo_steps"

The module is imported when ``judo.behave`` loads (so its ``@step`` definitions register) and its
source file is added to the step catalog (``judo steps``, ``judo validate``, MCP).
"""
import importlib
import importlib.util
from pathlib import Path
from typing import Dict, List

GROUP = "judo.plugins"


def _entry_points():
    try:
        from importlib.metadata import entry_points
    except ImportError:  # pragma: no cover
        return []
    eps = entry_points()
    if hasattr(eps, "select"):
        return list(eps.select(group=GROUP))
    return list(eps.get(GROUP, []))


def discover() -> List[Dict[str, str]]:
    """[{name, module, file}] for every installed plugin (no import)."""
    found = []
    for ep in _entry_points():
        module = ep.value.split(":")[0]
        try:
            spec = importlib.util.find_spec(module)
            origin = spec.origin if spec else None
        except (ImportError, ValueError):
            origin = None
        found.append({"name": ep.name, "module": module, "file": origin or ""})
    return found


def load_all() -> List[str]:
    """Import every plugin; failures are reported, never raised."""
    loaded = []
    for p in discover():
        try:
            importlib.import_module(p["module"])
            loaded.append(p["name"])
        except Exception as exc:  # a broken plugin must not break the framework
            print(f"⚠ Judo plugin '{p['name']}' failed to load: {exc}")
    return loaded


def plugin_files() -> List[Path]:
    return [Path(p["file"]) for p in discover() if p["file"].endswith(".py")]
