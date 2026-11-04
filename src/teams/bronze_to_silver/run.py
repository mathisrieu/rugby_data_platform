import logging
from pathlib import Path

from src.config import load_config
from src.teams.bronze_to_silver.write_teams_rosters import write_teams_rosters_file
from src.utils.logging import setup_logging


def run(ENV : str) -> None :

    # -------------- Load environment values ----------------------
    env = ENV if len(ENV) > 1 else "DEV"
    config = load_config(env)

    # -------------- Logging configuration ----------------------
    setup_logging(config.LOGS_PATH, Path(__file__).parent)
    logger = logging.getLogger(__name__)

    logger.info("*** Lauching pipeline ***")


    # generate the team rosters file
    write_teams_rosters_file(config.BRONZE_PATH, config.SILVER_PATH)



#run("INT")