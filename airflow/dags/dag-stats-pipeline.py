
from datetime import datetime

import docker
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.task_group import TaskGroup
from docker.types import Mount


# ---------------------------------------------------------------------
# Configuration Docker
# ---------------------------------------------------------------------

IMAGE_NAME = "ghcr.io/mathisrieu/rugby-data-stats"
IMAGE_TAG = "latest"
IMAGE_REFERENCE = f"{IMAGE_NAME}:{IMAGE_TAG}"

DOCKER_URL = "ssh://azureuser@172.16.0.5"

DOCKER_KWARGS = dict(
    image="{{ ti.xcom_pull(task_ids='prepare_docker_image') }}",
    docker_url=DOCKER_URL,
    auto_remove="success",
    mount_tmp_dir=False,
    mem_limit="800m",
    pool="worker_pool",
    force_pull=False,
    mounts=[
        Mount(
            source="/media/projects/rugby_data_platform",
            target="/app/data",
            type="bind",
        ),
    ],
    environment={
        # Secrets éventuellement transmis via les Variables Airflow
        # "DB_PASSWORD": "{{ var.value.DB_PASSWORD }}",
    },
)


# ---------------------------------------------------------------------
# Compétitions et saisons
# ---------------------------------------------------------------------

COMPETITION_SEASONS = {
    "top-14": ("2026-2027",),
    "pro-d2": ("2026-2027",),
    "premiership": ("2026-2027",),
    "champions-cup": ("2026-2027",),
    "challenge-cup": ("2026-2027",),
    "urc": ("2026-2027",),
}


# ---------------------------------------------------------------------
# Étapes ETL
# ---------------------------------------------------------------------

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


# ---------------------------------------------------------------------
# Préparation de l'image Docker sur VM-2
# ---------------------------------------------------------------------

def prepare_docker_image():
    client = docker.DockerClient(base_url=DOCKER_URL,use_ssh_client=True,)

    try:
        client.images.pull(
            IMAGE_NAME,
            tag=IMAGE_TAG,
        )

        print(f"Image récupérée : {IMAGE_REFERENCE}")

        # Retourne la référence complète.
        # Airflow la stocke automatiquement dans XCom.
        return IMAGE_REFERENCE

    finally:
        client.close()


# ---------------------------------------------------------------------
# Création des groupes de tâches
# ---------------------------------------------------------------------

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
                    "python",
                    "-m",
                    "src.utils.project_task",
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


# ---------------------------------------------------------------------
# Création des DAGs
# ---------------------------------------------------------------------

def create_competition_season_dag(
    competition: str,
    season: str,
) -> DAG:

    dag_id = f"stats_{competition}_{season}"

    with DAG(
        dag_id=dag_id,
        start_date=datetime(2025, 1, 1),
        schedule=None,
        catchup=False,
        max_active_runs=1,
        tags=["stats", competition, season],
    ) as dag:

        # 1. Téléchargement de l'image sur VM-2
        prepare_image = PythonOperator(
            task_id="prepare_docker_image",
            python_callable=prepare_docker_image,
        )

        # 2. Création des groupes ETL
        groups = {
            group_id: create_task_group(
                group_id,
                steps,
                competition,
                season,
            )
            for group_id, steps in TASK_GROUPS.items()
        }

        # 3. Ordonnancement
        prepare_image >> groups["calendar"]

        groups["calendar"] >> groups["players_per_match"]
        groups["players_per_match"] >> groups["player_stats"]

    return dag


# ---------------------------------------------------------------------
# Instanciation des DAGs
# ---------------------------------------------------------------------

for competition, seasons in COMPETITION_SEASONS.items():

    for season in seasons:

        competition_dag = create_competition_season_dag(
            competition,
            season,
        )

        globals()[competition_dag.dag_id] = competition_dag
