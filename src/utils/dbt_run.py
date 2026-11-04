import logging
import subprocess

logger = logging.getLogger(__name__)


def dbt_run (dbt_model: str, dbt_vars: dict):

    command = f"dbt run --select {dbt_model} --vars '{dbt_vars}'"

    # Execute the command
    try:
        subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        logger.info(f"dbt model '{dbt_model}' executing with success")


    except subprocess.CalledProcessError:

        logger.exception(f"Error during execution of the dbt model '{dbt_model}")
        raise



# values for test
# dbt_run("silver",
#         {"target_player_name": "matthias-haddad",
#         "team": "la-rochelle",
#         "match_label": "toulon-la-rochelle",
#         "is_the_first_file": 1,
#         "BRONZE_PATH": "/Volumes/rugby_data/DEV/data/bronze",
#         "SILVER_PATH": "/Volumes/rugby_data/DEV/data/silver"})