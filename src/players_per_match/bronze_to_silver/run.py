import logging
from pathlib import Path

from src.config import load_config
from src.players_per_match.bronze_to_silver.transform_players_per_match import (
    transform_players_per_match,
)
from src.utils.logging import setup_logging


def run(ENV : str, competition:str, season:str) -> None:

    # -------------- Load environment values ----------------------
    env = ENV if len(ENV) > 1 else "DEV"
    config = load_config(env)

    # -------------- Logging configuration ----------------------
    setup_logging(config.LOGS_PATH, Path(__file__).parent)
    logger = logging.getLogger(__name__)


    logger.info("**** Launching pipeline ****")


    # for each match to process (where exists flag file in bronze match folder):

    season_folder = config.BRONZE_PATH / Path(f"players_per_match/{competition}/saison-{season}")


    for match_folder in season_folder.rglob("*") :

        if match_folder.is_dir() and (match_folder / "to_do.flag").is_file():

            #transformations on the file (bronze to silver)
            try:
                transform_players_per_match(match_folder, config.BRONZE_PATH, config.SILVER_PATH)

                (match_folder / "to_do.flag").unlink()
                logger.info(f"bronze->silver OK for this match : {match_folder}")

            except Exception : # noqa: BLE001
                logger.warning(f"Error during function 'transform_players_per_match' for this match {match_folder}")



    logger.info("**** Pipeline done ****")



#run("INT", "top-14", "2026-2027")


