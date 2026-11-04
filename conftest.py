"""Configuration commune des tests : hermétiques (pas de réseau, Airflow isolé)."""

import os
import socket
import tempfile

import pytest

# Doit être fait AVANT tout import d'Airflow. Affectation directe (et non
# setdefault) : les tests ne doivent jamais toucher à l'Airflow local du dev.
os.environ["AIRFLOW_HOME"] = tempfile.mkdtemp(prefix="airflow_tests_")
os.environ["AIRFLOW__CORE__LOAD_EXAMPLES"] = "False"
os.environ["AIRFLOW__CORE__UNIT_TEST_MODE"] = "True"
os.environ["AIRFLOW_VAR_ENV"] = "INT"  # lu par Variable.get("ENV") dans les DAGs
os.environ["RUGBY_ENV"] = "INT"


@pytest.fixture(autouse=True, scope="session")
def _block_network():
    """Interdit tout accès réseau (scraping, SharePoint...) pendant les tests."""

    def _blocked(*args, **kwargs):
        raise RuntimeError("Accès réseau interdit pendant les tests")

    patcher = pytest.MonkeyPatch()
    patcher.setattr(socket.socket, "connect", _blocked)
    patcher.setattr(socket.socket, "connect_ex", _blocked)
    yield
    patcher.undo()
