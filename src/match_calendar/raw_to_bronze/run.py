import json
import logging
from pathlib import Path

from config import load_config
from match_calendar.raw_to_bronze.scrap_calendar import scrap_calendar
from utils.logging import setup_logging


def run(ENV:str, competition:str, season:str) -> None:


    # -------------- Load environment values ---------------------------------------
    env = ENV if len(ENV) > 1 else "DEV"
    config = load_config(env)

    # -------------- Logging configuration ----------------------
    setup_logging(config.LOGS_PATH, Path(__file__).parent)
    logger = logging.getLogger(__name__)


    logger.info("**** Launching pipeline ****")


    # -------------- Scrapping of the calendar -------------------------------------
    try:
        matches = scrap_calendar(competition)

    except Exception:
        logger.exception("Error during scrapping of the calendar")


    # -------------- Writing the json bronze calendar file -------------------------

    path_calendar = config.BRONZE_PATH / Path(f"calendar/{competition}/{season}")

    Path(path_calendar).mkdir(parents=True, exist_ok=True)

    with open(path_calendar / "calendar_bronze.json", "w", encoding="utf-8") as f:
        json.dump(matches, f, indent=4, ensure_ascii=False)

    logger.info(f"{len(matches)} games extracted → {path_calendar}")

    logger.info("**** Pipeline done ****")



# run("INT", "top-14", "2026-2027")