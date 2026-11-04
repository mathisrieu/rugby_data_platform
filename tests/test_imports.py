"""Importer un module ne doit avoir aucun effet de bord (scraping, écriture...).

Chaque module de src/ est importé réseau coupé (voir conftest.py). Un appel
oublié au niveau module, comme un `scrap_calendar()` en bas de fichier,
ferait échouer ce test au lieu de déclencher un scraping à chaque parsing de DAG.
"""

import importlib
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[1] / "src"


def _module_names() -> list[str]:
    names = []
    for path in sorted(SRC.rglob("*.py")):
        relative = path.relative_to(SRC).with_suffix("")
        parts = relative.parts[:-1] if relative.name == "__init__" else relative.parts
        if parts:
            names.append(".".join(parts))
    return names


@pytest.mark.parametrize("module_name", _module_names())
def test_module_imports_cleanly(module_name: str):
    importlib.import_module(module_name)
