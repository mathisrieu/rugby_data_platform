"""Les DAGs doivent se charger sans erreur (c'est ce que fait le scheduler Airflow)."""

from pathlib import Path

import pytest
from airflow.models import DagBag

DAGS_FOLDER = Path(__file__).resolve().parents[1] / "airflow" / "dags"


@pytest.fixture(scope="module")
def dagbag() -> DagBag:
    return DagBag(dag_folder=str(DAGS_FOLDER), include_examples=False)


def test_dags_import_without_errors(dagbag: DagBag):
    errors = {
        Path(file).name: message.strip().splitlines()[-1]
        for file, message in dagbag.import_errors.items()
    }
    assert not errors, f"Erreurs d'import de DAG : {errors}"


def test_dags_are_found(dagbag: DagBag):
    assert dagbag.dags, f"Aucun DAG trouvé dans {DAGS_FOLDER}"


def test_every_dag_has_tasks(dagbag: DagBag):
    empty = [dag_id for dag_id, dag in dagbag.dags.items() if not dag.tasks]
    assert not empty, f"DAGs sans tâche : {empty}"
