#from concurrent.futures import ThreadPoolExecutor
import json
import logging
from pathlib import Path

import pandas as pd

from src.config import load_config
from src.player_stats.raw_to_bronze.error_handling import write_error_file
from src.player_stats.raw_to_bronze.scrap_player_stats import scrap_player_stats
from src.recovering.resolve_scrapping_errors import resolve_scrapping_errors
from src.utils.logging import setup_logging


def recovering_run(ENV:str) -> None:

    # Load environment values ----------------------
    env = ENV if len(ENV) > 1 else "DEV"
    config = load_config(env)

    # -------------- Logging configuration ----------------------
    setup_logging(config.LOGS_PATH, Path(__file__).parent)
    logger = logging.getLogger(__name__)


    logger.info("** Launching recovering pipeline **")

    resolve_scrapping_errors(config.ERRORS_PATH, config.SILVER_PATH)

    scrapping_errors_filepath = config.ERRORS_PATH / "scrapping_errors.csv"

    df = pd.read_csv(scrapping_errors_filepath, delimiter=',')

    scrapping_errors_filepath.unlink(missing_ok=True)

    players = df[["player_name","team_name", "competition", "competition_name", "season"]].drop_duplicates().values.tolist()


    with open (config.SILVER_PATH / Path("teams/teams_rosters.json"), "r", encoding='utf-8') as f:
        team_rosters = json.load(f)

    for player in players :

        player_name = player[0]
        team_name = player[1]
        competition = player[2]
        competition_name = player[3]
        season = player[4]


        for team in team_rosters :
            if team.get("team")==team_name:
                for player in team["players"]:
                    if player.get("player_name")==player_name:
                        player_url = player.get("player_url")


        # scrapping player stats

        try:
            scrap_player_stats(player_name, team_name, player_url, competition, competition_name, season, config.BRONZE_PATH)
            logger.info(f"Scrapping success for player : {player_name}")


        except Exception as error: # noqa: BLE001
            logger.error(f"Scrapping error for player : {player_name}. Error : {error}")
            write_error_file(player_name, team_name, player_url, competition, competition_name, season, error, config.ERRORS_PATH)



    logger.info("** Recovering pipeline done **")



#recovering_run("DEV")


