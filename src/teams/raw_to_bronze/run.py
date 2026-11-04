
# extraction script for the list of player of a team
# source -> bronze

import logging
from pathlib import Path

import pandas as pd

from src.config import load_config
from src.teams.raw_to_bronze.scrap_team_roster import scrap_team_roster
from src.utils.logging import setup_logging


def run(ENV: str) -> None :

    # -------------- Load environment values ----------------------
    env = ENV if len(ENV) > 1 else "DEV"
    config = load_config(env)

    # -------------- Logging configuration ----------------------
    setup_logging(config.LOGS_PATH, Path(__file__).parent)
    logger = logging.getLogger(__name__)

    logger.info("*** Lauching pipeline ***")

    # retrieve list of teams
    teams_list_filepath = config.CONTEXT_PATH / "teams.csv"

    teams = pd.read_csv(teams_list_filepath, delimiter = ";")


    # for each team, scrap the player list, and team metadatas
    for team in teams:
        scrap_team_roster(config.BRONZE_PATH, team)

run("DEV")