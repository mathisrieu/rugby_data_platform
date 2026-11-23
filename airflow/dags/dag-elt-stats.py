# Ce DAG gere le pipeline de recuperation des stats (recuperation des matchs joués, recuperation des joueurs pour chacun des matchs joués, recuperation des stats pour chacun de ces joueurs)

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from src.utils.project_task import run_project_task

with DAG(
    dag_id="dag-elt-stats",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False
) as dag:
    

    player_stats_raw_to_bronze = PythonOperator(
        task_id="player_stats_raw_to_bronze",
        python_callable=run_project_task,
        op_args=["player_stats.raw_to_bronze.run", "{{ var.value.ENV }}"]
    )

    player_stats_bronze_to_silver = PythonOperator(
        task_id="player_stats_bronze_to_silver",
        python_callable=run_project_task,
        op_args=["player_stats.bronze_to_silver.run", "{{ var.value.ENV }}"]
    )

    player_stats_silver_to_gold = PythonOperator(
        task_id="player_stats_silver_to_gold",
        python_callable=run_project_task,
        op_args=["player_stats.silver_to_gold.run", "{{ var.value.ENV }}"]
    )


    player_stats_raw_to_bronze >> player_stats_bronze_to_silver >> player_stats_silver_to_gold
