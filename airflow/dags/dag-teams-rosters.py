# Cette tâche permet de récupérer la liste des joueurs des équipes de top 14
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.models import Variable

from src.teams.raw_to_bronze.run import run as raw_to_bronze
from src.teams.bronze_to_silver.run import run as bronze_to_silver
#from src.teams.silver_to_gold.run import run as silver_to_gold


ENV = Variable.get("ENV")


with DAG(
    dag_id="teams-rosters",
    start_date=datetime(2025, 1, 1),
    schedule = None,
    #schedule_interval="0 0 * 4-6 *", #Trigger de lancement quotidien entre le 01/04 et le 30/06 (période de tranferts)
    catchup=False
) as dag:
    

    teams_rosters_raw_to_bronze = PythonOperator(
        task_id="teams_rosters_raw_to_bronze",
        python_callable=raw_to_bronze,
        op_args=[ENV]
    )

    teams_rosters_bronze_to_silver = PythonOperator(
        task_id="teams_rosters_bronze_to_silver",
        python_callable=bronze_to_silver,
        op_args=[ENV]
    )


    teams_rosters_raw_to_bronze >> teams_rosters_bronze_to_silver

