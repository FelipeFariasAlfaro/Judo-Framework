#!/usr/bin/env python
"""
Manual fallback to publish Judo Framework to PyPI.

The normal way to release is the GitHub Actions pipeline (.github/workflows/publish.yml):
bump the version in pyproject.toml and judo/__init__.py, commit, then
    git tag -a vX.Y.Z -m "Judo Framework X.Y.Z" && git push origin vX.Y.Z

This script needs `pip install build twine` and PyPI credentials (~/.pypirc or TWINE_* env vars).
Usage: python publish.py
"""

import glob
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def version() -> str:
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    return re.search(r'^version = "([^"]+)"', text, re.M).group(1)


def run(args, desc):
    print(f"\n{'=' * 50}\n{desc}\n{'=' * 50}")
    if subprocess.run(args, cwd=ROOT).returncode != 0:
        print(f"❌ Failed: {desc}")
        sys.exit(1)
    print(f"✅ Done: {desc}")


def main():
    v = version()
    print("\n" + "=" * 50)
    print(f"JUDO FRAMEWORK - PUBLISHING TO PyPI v{v}")
    print("=" * 50)

    for folder in ("build", "dist", "judo_framework.egg-info"):
        shutil.rmtree(ROOT / folder, ignore_errors=True)

    run([sys.executable, "-m", "build"], "Building distribution packages")
    files = glob.glob(str(ROOT / "dist" / "*"))
    run([sys.executable, "-m", "twine", "check", *files], "Checking distribution")
    run([sys.executable, "-m", "twine", "upload", "--skip-existing", *files], "Uploading to PyPI")

    print("\n✅ Published successfully!")
    print(f"Install with: pip install judo-framework=={v}")


if __name__ == "__main__":
    main()
