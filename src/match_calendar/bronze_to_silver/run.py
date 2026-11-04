import json
import logging
import os
import sys
from pathlib import Path

from config import load_config
from match_calendar.bronze_to_silver.define_match_to_load import define_match_to_load
from match_calendar.bronze_to_silver.transform_calendar import transform_calendar
from utils.logging import setup_logging


def run(ENV: str, competition:str, season:str) -> None :

    # -------------- Load environment values ----------------------
    env = ENV if len(ENV) > 1 else "DEV"
    config = load_config(env)

    # -------------- Logging configuration ----------------------
    setup_logging(config.LOGS_PATH, Path(__file__).parent)
    logger = logging.getLogger(__name__)


    logger.info("**** Launching pipeline ****")


    # Create calendar folder if not exist ------------------------------------------

    Path(config.SILVER_PATH / f"calendar/{competition}/{season}").mkdir(parents=True, exist_ok=True)


    # Define matches to load -------------------------------------------------------

    match_to_add_filepath = config.TMP_PATH / Path(f"match_to_add_{competition}.csv")

    try:
        define_match_to_load(config.BRONZE_PATH, config.SILVER_PATH, match_to_add_filepath, competition, season)

    except Exception :
        logger.exception("Error during function 'define_match_to_load' ")

    # Exit if no matches to load ---------------------------------------------------

    if not os.path.exists(match_to_add_filepath):
        logger.warning("No match to add")
        logger.info("**** Pipeline done ****")
        sys.exit()


    # Transformations on calendar --------------------------------------------------

    df_data = transform_calendar(config.BRONZE_PATH, config.SILVER_PATH, match_to_add_filepath, competition, season)


    # Creation of the calendar json silver file ---------------------------------------------

    data = df_data.to_json(orient="records", force_ascii=False)
    json_data = json.loads(data)

    if json_data:

        with open (config.SILVER_PATH / Path(f"calendar/{competition}/{season}/calendar_silver.json"), "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)



    # Remove temporary file ----------

    os.remove(match_to_add_filepath)


    logger.info("**** Pipeline done ****")



#run("INT", "top-14", "2026-2027")