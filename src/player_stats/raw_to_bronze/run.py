#from concurrent.futures import ThreadPoolExecutor
import logging
from pathlib import Path

import pandas as pd

from src.config import load_config
from src.player_stats.raw_to_bronze.error_handling import write_error_file
from src.player_stats.raw_to_bronze.processing import (
    define_matches_to_process,
    define_players_to_process,
    update_calendar,
)
from src.player_stats.raw_to_bronze.recovering_run import recovering_run
from src.player_stats.raw_to_bronze.scrap_player_stats import scrap_player_stats
from src.utils.logging import setup_logging


def run(ENV:str, competition:str, season:str) -> None:

    # Load environment values ----------------------
    env = ENV if len(ENV) > 1 else "DEV"
    config = load_config(env)

    # -------------- Logging configuration ----------------------
    setup_logging(config.LOGS_PATH, Path(__file__).parent)
    logger = logging.getLogger(__name__)


    logger.info("**** Launching pipeline ****")

    try:
        matches_to_process = define_matches_to_process(config.SILVER_PATH)
        logger.info(f"Matches to process : {matches_to_process}")
    except Exception :
        logger.exception("Error during function 'define_matches_to_process' ")


    for match in matches_to_process:
        
        match_folder = Path(match).name

        players_to_process = define_players_to_process(match, config.SILVER_PATH)

        for player_record in players_to_process:

            player = player_record["player_name"]
            team_name = player_record["team_name"]
            player_url = player_record["player_url"]


            # scrapping player stats
            df = pd.read_csv(config.CONTEXT_PATH / "competitions_names.csv", delimiter=';')
            df = df["rugbypass_name"][df["all_rugby_name"]==competition]
            competition_name = str(df.iloc[0])


            try:
                scrap_player_stats(player, team_name, player_url, competition, competition_name, season, config.BRONZE_PATH)
                logger.info(f"Scrapping success for player : {player}")

            except Exception as error: # noqa: BLE001
                logger.error(f"Scrapping error for player : {player}. Error : {error}")
                write_error_file(player, team_name, player_url, competition, competition_name, season, error, config.ERRORS_PATH)


        # delete flag file from the match folder
        Path(f"{match}/to_do.flag").unlink()


        update_calendar(config.SILVER_PATH, match_folder, competition, season)


    recovering_run(ENV)


    logger.info("**** Pipeline done ****")



#run("INT", "top-14", "2026-2027")


