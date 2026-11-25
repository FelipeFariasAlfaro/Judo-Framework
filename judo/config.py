"""
Typed project configuration (``config/judo.yaml`` or ``judo.yaml``).

    default_env: dev
    timeout: 30
    verify_ssl: true
    proxy: ""
    retries: 0
    environments:
      dev:  { baseUrl: "https://api-dev.example.com", timeout: 10 }
      prod: { baseUrl: "https://api.example.com" }

``apply_to_environment`` exports the selected values as the JUDO_* variables the framework
already understands, without overriding values the user set explicitly.
"""
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

_TYPES = {"default_env": str, "timeout": (int, float), "verify_ssl": bool, "proxy": str,
          "retries": int, "baseUrl": str, "strict_variables": bool}
_ENV_KEYS = {"baseUrl", "timeout", "verify_ssl", "proxy", "retries", "strict_variables"}
_TOP_KEYS = _ENV_KEYS | {"default_env", "environments"}

CANDIDATES = ("config/judo.yaml", "judo.yaml", "config/judo.yml", "judo.yml")


def find_config(root: Optional[Path] = None) -> Optional[Path]:
    root = root or Path.cwd()
    for c in CANDIDATES:
        if (root / c).exists():
            return root / c
    return None


def load(path: Path) -> Dict[str, Any]:
    import yaml
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def validate(cfg: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if not isinstance(cfg, dict):
        return ["Configuration must be a mapping"]

    def check(block: Dict[str, Any], where: str, allowed):
        for k, v in block.items():
            if k not in allowed:
                errors.append(f"{where}: unknown key '{k}'")
                continue
            t = _TYPES.get(k)
            if t and (not isinstance(v, t) or (t is not bool and isinstance(v, bool))):
                errors.append(f"{where}.{k}: expected {getattr(t, '__name__', t)}, got {type(v).__name__}")
        if isinstance(block.get("timeout"), (int, float)) and block["timeout"] < 0:
            errors.append(f"{where}.timeout: must be >= 0")

    check({k: v for k, v in cfg.items() if k != "environments"}, "config", _TOP_KEYS)
    envs = cfg.get("environments") or {}
    if not isinstance(envs, dict):
        errors.append("config.environments: must be a mapping")
        envs = {}
    for name, block in envs.items():
        if not isinstance(block, dict):
            errors.append(f"environments.{name}: must be a mapping")
            continue
        check(block, f"environments.{name}", _ENV_KEYS)
    default = cfg.get("default_env")
    if default and default not in envs:
        errors.append(f"config.default_env: '{default}' is not defined in environments")
    return errors


def resolve(cfg: Dict[str, Any], env: Optional[str] = None) -> Dict[str, Any]:
    """Top-level values overridden by the selected environment block."""
    merged = {k: v for k, v in cfg.items() if k in _ENV_KEYS}
    name = env or cfg.get("default_env")
    if name:
        block = (cfg.get("environments") or {}).get(name)
        if block is None:
            raise ValueError(f"Environment '{name}' is not defined in the configuration")
        merged.update(block)
        merged["env"] = name
    return merged


def apply_to_environment(values: Dict[str, Any], environ=None) -> Dict[str, str]:
    environ = os.environ if environ is None else environ
    mapping = {"baseUrl": "JUDO_BASE_URL", "timeout": "JUDO_TIMEOUT", "verify_ssl": "JUDO_VERIFY_SSL",
               "proxy": "JUDO_PROXY", "retries": "JUDO_RETRIES", "strict_variables": "JUDO_STRICT_VARS",
               "env": "JUDO_ENV"}
    applied = {}
    for key, var in mapping.items():
        if key in values and var not in environ and values[key] not in (None, ""):
            val = values[key]
            environ[var] = str(val).lower() if isinstance(val, bool) else str(val)
            applied[var] = environ[var]
    return applied
