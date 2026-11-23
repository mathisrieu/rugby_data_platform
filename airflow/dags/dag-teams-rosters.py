# Cette tâche permet de récupérer la liste des joueurs des équipes de top 14
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from src.utils.project_task import run_project_task
#from src.teams.silver_to_gold.run import run as silver_to_gold


with DAG(
    dag_id="teams-rosters",
    start_date=datetime(2025, 1, 1),
    schedule = None,
    #schedule_interval="0 0 * 4-6 *", #Trigger de lancement quotidien entre le 01/04 et le 30/06 (période de tranferts)
    catchup=False
) as dag:
    

    teams_rosters_raw_to_bronze = PythonOperator(
        task_id="teams_rosters_raw_to_bronze",
        python_callable=run_project_task,
        op_args=["src.teams.raw_to_bronze.run", "{{ var.value.ENV }}"]
    )

    teams_rosters_bronze_to_silver = PythonOperator(
        task_id="teams_rosters_bronze_to_silver",
        python_callable=run_project_task,
        op_args=["src.teams.bronze_to_silver.run", "{{ var.value.ENV }}"]
    )


    teams_rosters_raw_to_bronze >> teams_rosters_bronze_to_silver
