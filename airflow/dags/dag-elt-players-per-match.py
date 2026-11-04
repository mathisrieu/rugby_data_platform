# Ce DAG gere le pipeline de recuperation des stats (recuperation des matchs joués, recuperation des joueurs pour chacun des matchs joués, recuperation des stats pour chacun de ces joueurs)

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from datetime import datetime

from src.players_per_match.raw_to_bronze.run import run as raw_to_bronze
from src.players_per_match.bronze_to_silver.run import run as bronze_to_silver
#from src.players_per_match.silver_to_gold.run import run as silver_to_gold


ENV = Variable.get("ENV")


with DAG(
    dag_id="dag-elt-players-per-match",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False
) as dag:
    

    players_per_match_raw_to_bronze = PythonOperator(
        task_id="players_per_match_raw_to_bronze",
        python_callable=raw_to_bronze,
        op_args=[ENV]
    )

    players_per_match_bronze_to_silver = PythonOperator(
        task_id="players_per_match_bronze_to_silver",
        python_callable=bronze_to_silver,
        op_args=[ENV]
    )

    # players_per_match_silver_to_gold = PythonOperator(
    #     task_id="players_per_match_silver_to_gold",
    #     python_callable=silver_to_gold,
    #     op_args=[ENV]
    # )


    players_per_match_raw_to_bronze >> players_per_match_bronze_to_silver #>> players_per_match_silver_to_gold


