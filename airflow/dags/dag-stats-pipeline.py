from datetime import datetime

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.task_group import TaskGroup
from docker.types import Mount

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
        ("raw_to_bronze", "src.match_calendar.raw_to_bronze.run"),
        ("bronze_to_silver", "src.match_calendar.bronze_to_silver.run"),
        ("silver_to_gold", "src.match_calendar.silver_to_gold.run"),
    ),
    "players_per_match": (
        ("raw_to_bronze", "src.players_per_match.raw_to_bronze.run"),
        ("bronze_to_silver", "src.players_per_match.bronze_to_silver.run"),
        ("silver_to_gold", "src.players_per_match.silver_to_gold.run"),
    ),
    "player_stats": (
        ("raw_to_bronze", "src.player_stats.raw_to_bronze.run"),
        ("bronze_to_silver", "src.player_stats.bronze_to_silver.run"),
        ("silver_to_gold", "src.player_stats.silver_to_gold.run"),
    ),
}

DOCKER_KWARGS = dict(
    image="{{ var.value.PROJECT_IMAGE }}",   # ex. ghcr.io/moi/projet:1.4
    docker_url="ssh://azureuser@74.152.65.24",   # IP privée de la VM d'exécution
    auto_remove="success",
    mount_tmp_dir=False,
    mem_limit="800m",
    pool="worker_pool",                       # limite les conteneurs simultanés
    mounts=[                                  # voir le point crucial ci-dessous
        Mount(source="/media/projects/rugby_data_platform", target="/app/data", type="bind"),
    ],
    environment={
        # secrets lus dans les Variables Airflow, à adapter à votre code
        # "DB_PASSWORD": "{{ var.value.DB_PASSWORD }}",
    },
)


def create_task_group(
    group_id: str,
    steps: tuple[tuple[str, str], ...],
    competition: str,
    season: str,
) -> TaskGroup:
    with TaskGroup(group_id=group_id) as task_group:
        previous_task = None
        for task_id, module_path in steps:
            task = DockerOperator(
                task_id=task_id,
                command=[
                    "python", "-m", "src.utils.project_task",
                    module_path,
                    "{{ var.value.ENV }}",
                    competition,
                    season,
                ],
                **DOCKER_KWARGS,
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