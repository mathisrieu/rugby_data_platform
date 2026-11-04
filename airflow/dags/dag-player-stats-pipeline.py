
# Ce DAG gere le pipeline complet de recuperation des statistiques pour une competition donnée:
# 1. Recuperation du calendrier des matchs
# 2. Recuperation des joueurs pour chaque match
# 3. Recuperation des statistiques de chaque joueur

from datetime import datetime

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup


# ============================================================
# IMPORTS : CALENDAR
# ============================================================

from match_calendar.raw_to_bronze.run import (
    run as calendar_raw_to_bronze,
)
from match_calendar.bronze_to_silver.run import (
    run as calendar_bronze_to_silver,
)
# from match_calendar.silver_to_gold.run import (
#     run as calendar_silver_to_gold,
# )


# ============================================================
# IMPORTS : PLAYERS PER MATCH
# ============================================================

from src.players_per_match.raw_to_bronze.run import (
    run as players_per_match_raw_to_bronze,
)
from src.players_per_match.bronze_to_silver.run import (
    run as players_per_match_bronze_to_silver,
)
# from src.players_per_match.silver_to_gold.run import (
#     run as players_per_match_silver_to_gold,
# )


# ============================================================
# IMPORTS : PLAYER STATS
# ============================================================

from player_stats.raw_to_bronze.run import (
    run as player_stats_raw_to_bronze,
)
from player_stats.bronze_to_silver.run import (
    run as player_stats_bronze_to_silver,
)
from player_stats.silver_to_gold.run import (
    run as player_stats_silver_to_gold,
)



# ============================================================
# DAG
# ============================================================

with DAG(
    dag_id="player-stats-pipeline",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    # --------------------------------------------------------
    # TASK GROUP : CALENDAR
    # --------------------------------------------------------

    with TaskGroup(group_id="calendar") as calendar_group:

        calendar_raw_to_bronze_task = PythonOperator(
            task_id="raw_to_bronze",
            python_callable=calendar_raw_to_bronze,
            op_args=[
                "{{ dag_run.conf['ENV'] }}",
                "{{ dag_run.conf['competition'] }}",
                "{{ dag_run.conf['season'] }}",
            ],
        )

        calendar_bronze_to_silver_task = PythonOperator(
            task_id="bronze_to_silver",
            python_callable=calendar_bronze_to_silver,
            op_args=[
                "{{ dag_run.conf['ENV'] }}",
                "{{ dag_run.conf['competition'] }}",
                "{{ dag_run.conf['season'] }}",
            ],
        )

        # calendar_silver_to_gold_task = PythonOperator(
        #     task_id="silver_to_gold",
        #     python_callable=calendar_silver_to_gold,
        #     op_args=[ENV],
        # )

        (
            calendar_raw_to_bronze_task
            >> calendar_bronze_to_silver_task
        )

        # Activer si silver_to_gold est disponible :
        # calendar_bronze_to_silver_task >> calendar_silver_to_gold_task


    # --------------------------------------------------------
    # TASK GROUP : PLAYERS PER MATCH
    # --------------------------------------------------------

    with TaskGroup(group_id="players_per_match") as players_per_match_group:

        players_per_match_raw_to_bronze_task = PythonOperator(
            task_id="raw_to_bronze",
            python_callable=players_per_match_raw_to_bronze,
            op_args=[
                "{{ dag_run.conf['ENV'] }}",
                "{{ dag_run.conf['competition'] }}",
                "{{ dag_run.conf['season'] }}",
            ],
        )

        players_per_match_bronze_to_silver_task = PythonOperator(
            task_id="bronze_to_silver",
            python_callable=players_per_match_bronze_to_silver,
            op_args=[
                "{{ dag_run.conf['ENV'] }}",
                "{{ dag_run.conf['competition'] }}",
                "{{ dag_run.conf['season'] }}",
            ],
        )

        # players_per_match_silver_to_gold_task = PythonOperator(
        #     task_id="silver_to_gold",
        #     python_callable=players_per_match_silver_to_gold,
        #     op_args=[ENV],
        # )

        (
            players_per_match_raw_to_bronze_task
            >> players_per_match_bronze_to_silver_task
        )

        # Activer si silver_to_gold est disponible :
        # players_per_match_bronze_to_silver_task >> players_per_match_silver_to_gold_task


    # --------------------------------------------------------
    # TASK GROUP : PLAYER STATS
    # --------------------------------------------------------

    with TaskGroup(group_id="player_stats") as player_stats_group:

        player_stats_raw_to_bronze_task = PythonOperator(
            task_id="raw_to_bronze",
            python_callable=player_stats_raw_to_bronze,
            op_args=[
                "{{ dag_run.conf['ENV'] }}",
                "{{ dag_run.conf['competition'] }}",
                "{{ dag_run.conf['season'] }}",
            ],
        )

        player_stats_bronze_to_silver_task = PythonOperator(
            task_id="bronze_to_silver",
            python_callable=player_stats_bronze_to_silver,
            op_args=[
                "{{ dag_run.conf['ENV'] }}",
                "{{ dag_run.conf['competition'] }}",
                "{{ dag_run.conf['season'] }}",
            ],
        )

        player_stats_silver_to_gold_task = PythonOperator(
            task_id="silver_to_gold",
            python_callable=player_stats_silver_to_gold,
            op_args=[
                "{{ dag_run.conf['ENV'] }}",
                "{{ dag_run.conf['competition'] }}",
                "{{ dag_run.conf['season'] }}",
            ],
        )

        (
            player_stats_raw_to_bronze_task
            >> player_stats_bronze_to_silver_task
            >> player_stats_silver_to_gold_task
        )


    # --------------------------------------------------------
    # DEPENDANCES ENTRE LES PIPELINES
    # --------------------------------------------------------

    calendar_group >> players_per_match_group >> player_stats_group
