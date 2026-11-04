# Ce DAG gere le pipeline de recuperation des stats (recuperation des matchs joués, recuperation des joueurs pour chacun des matchs joués, recuperation des stats pour chacun de ces joueurs)

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.models import Variable


from player_stats.raw_to_bronze.run import run as raw_to_bronze
from player_stats.bronze_to_silver.run import run as bronze_to_silver
from player_stats.silver_to_gold.run import run as silver_to_gold



ENV = Variable.get("ENV")


with DAG(
    dag_id="dag-elt-stats",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False
) as dag:
    

    player_stats_raw_to_bronze = PythonOperator(
        task_id="player_stats_raw_to_bronze",
        python_callable=raw_to_bronze,
        op_args=[ENV]
    )

    player_stats_bronze_to_silver = PythonOperator(
        task_id="player_stats_bronze_to_silver",
        python_callable=bronze_to_silver,
        op_args=[ENV]
    )

    player_stats_silver_to_gold = PythonOperator(
        task_id="player_stats_silver_to_gold",
        python_callable=silver_to_gold,
        op_args=[ENV]
    )


    player_stats_raw_to_bronze >> player_stats_bronze_to_silver >> player_stats_silver_to_gold


