
import logging
from pathlib import Path

from src.config import load_config
from src.player_stats.bronze_to_silver.processing import define_player_to_process
from src.player_stats.bronze_to_silver.transform import clean_json
from src.utils.logging import setup_logging


def run(ENV:str, competition:str, season:str) -> None :


    # -------------- Load environment values ----------------------
    env = ENV if len(ENV) > 1 else "DEV"
    config = load_config(env)

    # -------------- Logging configuration ----------------------
    setup_logging(config.LOGS_PATH, Path(__file__).parent)
    logger = logging.getLogger(__name__)


    logger.info("**** Launching pipeline ****")

    try:
        players_to_process = define_player_to_process(config.BRONZE_PATH, competition, season)

    except Exception :
        logger.exception("Error during function 'define_player_to_process' ")


    for player_to_process in players_to_process:
    

        logger.info(f"Launching cleaning pipeline (bronze to silver) for : {player_to_process}")
        
        #create silver folder if not exists
        player_folder = player_to_process.relative_to(config.BRONZE_PATH).parent
        Path(config.SILVER_PATH / player_folder).mkdir(parents=True, exist_ok=True)


        try:
            clean_json(player_to_process, config.BRONZE_PATH, config.SILVER_PATH)
            flag_file = next((config.BRONZE_PATH / player_folder).glob("*.flag"))
            if flag_file is not None:
                flag_file.unlink() # remove the flag file from bronze folder

            logger.info(f"cleaning function OK for : {player_folder}")


        except Exception: # noqa: BLE001
            logger.warning(f"cleaning function in error for player : {player_folder}")


    logger.info("**** Pipeline done ****")



#run("DEV", "top-14", "2026-2027")


