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


def test_statistics_dag_exists_for_each_configured_competition_season(dagbag: DagBag):
    expected_dag_ids = {
        f"stats_{competition}_2026-2027"
        for competition in (
            "top-14",
            "pro-d2",
            "premiership",
            "champions-cup",
            "challenge-cup",
            "urc",
        )
    }

    assert expected_dag_ids <= set(dagbag.dag_ids)
    assert "player-stats-pipeline" not in dagbag.dag_ids



def test_statistics_dags_share_pipeline_and_use_their_own_parameters(dagbag: DagBag):
    dag = dagbag.dags["stats_top-14_2026-2027"]
    assert dag is not None
    assert len(dag.tasks) == 10

    task = dag.get_task("calendar.raw_to_bronze")

    assert task.command == [
        "python",
        "-m",
        "src.utils.project_task",
        "src.match_calendar.raw_to_bronze.run",
        "{{ var.value.ENV }}",
        "top-14",
        "2026-2027",
    ]



def test_statistics_dag_dependencies_are_visible_in_each_dag(dagbag: DagBag):
    dag = dagbag.dags["stats_top-14_2026-2027"]
    assert dag is not None

    assert dag.get_task("calendar.raw_to_bronze").downstream_task_ids == {
        "calendar.bronze_to_silver"
    }
    assert dag.get_task("calendar.bronze_to_silver").downstream_task_ids == {
        "calendar.silver_to_gold"
    }
    assert dag.get_task("calendar.silver_to_gold").downstream_task_ids == {
        "players_per_match.raw_to_bronze"
    }
    assert dag.get_task("players_per_match.silver_to_gold").downstream_task_ids == {
        "player_stats.raw_to_bronze"
    }
