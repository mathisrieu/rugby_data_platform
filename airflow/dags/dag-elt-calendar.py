# Ce DAG gere le pipeline de recuperation des stats (recuperation des matchs joués, recuperation des joueurs pour chacun des matchs joués, recuperation des stats pour chacun de ces joueurs)

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from src.utils.project_task import run_project_task
#from match_calendar.silver_to_gold.run import run as silver_to_gold


with DAG(
    dag_id="dag-elt-calendar",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False
) as dag:
    

    calendar_raw_to_bronze = PythonOperator(
        task_id="calendar_raw_to_bronze",
        python_callable=run_project_task,
        op_args=["match_calendar.raw_to_bronze.run", "{{ var.value.ENV }}"]
    )

    calendar_bronze_to_silver = PythonOperator(
        task_id="calendar_bronze_to_silver",
        python_callable=run_project_task,
        op_args=["match_calendar.bronze_to_silver.run", "{{ var.value.ENV }}"]
    )

    # calendar_silver_to_gold = PythonOperator(
    #     task_id="calendar_silver_to_gold",
    #     python_callable=silver_to_gold,
    #     op_args=[ENV]
    # )


    calendar_raw_to_bronze >> calendar_bronze_to_silver #>> calendar_silver_to_gold
