import logging
from pathlib import Path

from src.config import load_config
from src.utils.dbt_run import dbt_run
from src.utils.logging import setup_logging


def run(ENV:str, competition:str, season:str) -> None :

    # -------------- Load environment values ----------------------
    env = ENV if len(ENV) > 1 else "DEV"
    config = load_config(env)

    # -------------- Logging configuration ----------------------
    setup_logging(config.LOGS_PATH, Path(__file__).parent)
    logger = logging.getLogger(__name__)


    logger.info("**** Launching pipeline ****")

    logger.info(f"Launching dbt transformation pipeline (silver to gold) for competition {competition} (season : {season})")

    #create silver folder if not exists
    Path(config.GOLD_PATH / "player_stats").mkdir(parents=True, exist_ok=True)


    dbt_model = "gold"
    dbt_vars = {"competition": competition,
                "season": season,
                "SILVER_PATH": str(config.SILVER_PATH),
                "GOLD_PATH": str(config.GOLD_PATH)
                }

    try:
        dbt_run(dbt_model, dbt_vars)
        logger.info(f"dbt run function OK for competition : {competition} (season : {season})")

    except Exception:
        logger.exception(f"dbt run function in error for competition : {competition} (season : {season})")
        raise


    logger.info("**** Pipeline done ****")



#run("DEV", "top-14", "2026-2027")