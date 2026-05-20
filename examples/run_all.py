"""Run every PSPhasor example script."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

EXAMPLES_DIR = Path(__file__).resolve().parent


def _load_module(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load example script: {path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    """Run all numbered examples."""

    for path in sorted(EXAMPLES_DIR.glob("[0-9][0-9]_*.py")):
        module = _load_module(path)
        print(f"Running {path.name}")
        module.main()


if __name__ == "__main__":
    main()
