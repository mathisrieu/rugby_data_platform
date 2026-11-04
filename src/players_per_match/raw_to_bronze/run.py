import logging
from pathlib import Path

from src.config import load_config
from src.players_per_match.raw_to_bronze.matches_to_process import matches_to_process
from src.players_per_match.raw_to_bronze.scrap_players_per_match import (
    scrap_players_per_match,
)
from src.utils.logging import setup_logging


def run(ENV: str, competition:str, season:str) -> None :


    # -------------- Load environment values ----------------------
    env = ENV if len(ENV) > 1 else "DEV"
    config = load_config(env)

    # -------------- Logging configuration ----------------------
    setup_logging(config.LOGS_PATH, Path(__file__).parent)
    logger = logging.getLogger(__name__)


    logger.info("**** Launching pipeline ****")


    # retrieve from calendar_silver.json the list of matches to process (where is_loaded = false)

    silver_path_calendar = config.SILVER_PATH / Path(f"calendar/{competition}/{season}/calendar_silver.json")

    try:
        df = matches_to_process(silver_path_calendar)
    except Exception :
        logger.exception("Error during function 'matches_to_process")


    # for each match :

    for match, home_team, away_team in zip(df["match_url"],df["equipe_domicile"],df["equipe_exterieur"]):

        # scrap player list for the match
        try:
            scrap_players_per_match(config.BRONZE_PATH, match, home_team, away_team, competition)
            logger.info(f"Scrapping done for player list of this match : {match}")
        except Exception: # noqa: BLE001
            logger.warning(f"Scrapping failed for player list of this match : {match}")


    logger.info("**** Pipeline done ****")




#run("INT", "top-14", "2026-2027")