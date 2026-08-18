"""Pytest bootstrap for the backend source tree."""

import sys
from importlib import import_module
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[1]
backend_root = str(BACKEND_ROOT)
if backend_root in sys.path:
    sys.path.remove(backend_root)
sys.path.insert(0, backend_root)

# Some pytest plugins import an unrelated top-level ``app`` module before test
# collection. Ensure test imports resolve to this repository's backend package.
sys.modules.pop("app", None)
import_module("app")
