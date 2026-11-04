from datetime import datetime

from airflow import DAG
from airflow.models import Variable
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

ENV = Variable.get("ENV")


COMPETITIONS = {
    "top-14": {
        "season": "2026-2027",
    },
    "pro-d2": {
        "season": "2026-2027",
    },
    "premiership": {
        "season": "2026-2027",
    },
    "champions-cup": {
        "season": "2026-2027",
    },
    "challenge-cup": {
        "season": "2026-2027",
    },
    "urc": {
        "season": "2026-2027",
    },
}

def create_competition_dag(competition, config):
    dag_id = f"stats_{competition}_{config['season']}"

    with DAG(
        dag_id=dag_id,
        start_date=datetime(2025, 1, 1),
        schedule=None,
        catchup=False,
        tags=["stats", competition, config['season']],
    ) as dag:

        TriggerDagRunOperator(
            task_id="run_pipeline",
            trigger_dag_id="player-stats-pipeline",
            conf={
                "ENV": ENV,
                "competition": competition,
                "season": config["season"],
            },
        )

    return dag


# create automaticly one dag per competition
for competition, config in COMPETITIONS.items():
    dag = create_competition_dag(competition, config)





# with DAG(
#     dag_id="stats_top-14_2026-2027",
#     start_date=datetime(2025, 1, 1),
#     schedule=None,
#     catchup=False,
# ) as dag:

#     run_pipeline = TriggerDagRunOperator(
#         task_id="run_pipeline",
#         trigger_dag_id="player-stats-pipeline",
#         conf={
#             "ENV": ENV,
#             "competition": "top-14",
#             "season": "2026-2027",
#         },
#     )