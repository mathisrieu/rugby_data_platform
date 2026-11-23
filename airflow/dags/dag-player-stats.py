from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup

from src.utils.project_task import run_project_task


COMPETITION_SEASONS = {
    "top-14": ("2026-2027",),
    "pro-d2": ("2026-2027",),
    "premiership": ("2026-2027",),
    "champions-cup": ("2026-2027",),
    "challenge-cup": ("2026-2027",),
    "urc": ("2026-2027",),
}

TASK_GROUPS = {
    "calendar": (
        ("raw_to_bronze", "match_calendar.raw_to_bronze.run"),
        ("bronze_to_silver", "match_calendar.bronze_to_silver.run"),
        ("silver_to_gold", "match_calendar.silver_to_gold.run"),
    ),
    "players_per_match": (
        ("raw_to_bronze", "src.players_per_match.raw_to_bronze.run"),
        ("bronze_to_silver", "src.players_per_match.bronze_to_silver.run"),
        ("silver_to_gold", "src.players_per_match.silver_to_gold.run"),
    ),
    "player_stats": (
        ("raw_to_bronze", "player_stats.raw_to_bronze.run"),
        ("bronze_to_silver", "player_stats.bronze_to_silver.run"),
        ("silver_to_gold", "player_stats.silver_to_gold.run"),
    ),
}


def create_task_group(
    group_id: str,
    steps: tuple[tuple[str, str], ...],
    competition: str,
    season: str,
) -> TaskGroup:
    with TaskGroup(group_id=group_id) as task_group:
        previous_task = None
        for task_id, module_path in steps:
            task = PythonOperator(
                task_id=task_id,
                python_callable=run_project_task,
                op_args=[
                    module_path,
                    "{{ var.value.ENV }}",
                    competition,
                    season,
                ],
            )
            if previous_task is not None:
                previous_task >> task
            previous_task = task

    return task_group


def create_competition_season_dag(competition: str, season: str) -> DAG:
    dag_id = f"stats_{competition}_{season}"

    with DAG(
        dag_id=dag_id,
        start_date=datetime(2025, 1, 1),
        schedule=None,
        catchup=False,
        max_active_runs=1,
        tags=["stats", competition, season],
    ) as dag:
        groups = {
            group_id: create_task_group(group_id, steps, competition, season)
            for group_id, steps in TASK_GROUPS.items()
        }

        groups["calendar"] >> groups["players_per_match"] >> groups["player_stats"]

    return dag


for competition, seasons in COMPETITION_SEASONS.items():
    for season in seasons:
        competition_dag = create_competition_season_dag(competition, season)
        globals()[competition_dag.dag_id] = competition_dag
