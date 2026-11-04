import logging
import os
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

def define_match_to_load(BRONZE_PATH, SILVER_PATH, match_to_load_filepath, competition:str, season:str):


    bronze_path_calendar = BRONZE_PATH / Path(f"calendar/{competition}/{season}/calendar_bronze.json")
    silver_path_calendar = SILVER_PATH / Path(f"calendar/{competition}/{season}/calendar_silver.json")

    df_bronze = pd.read_json(bronze_path_calendar)


    if silver_path_calendar.exists():
        df_silver = pd.read_json(silver_path_calendar)
    else:
        df_silver = pd.DataFrame()
        

    if not df_silver.empty:

    # match_list_bronze = []
    # match_list_bronze.append(df_bronze["url"])

        match_list_silver = ""
        for match_silver in df_silver["match_url"]:
            match_list_silver += f"{match_silver} ; "

        # match_already_played = ""
        # for match_url, result in zip(df_silver["match_url"],df_silver["result"]): #cette partie est à modifier puisque on a dit que les matchs sans resultat (non joués) ne se retrouvent pas dans le silver
        #     if result != None:
        #         match_already_played += f"{match_url} ; "

        match_not_played_yet = ""
        for score_match_bronze, match_url in zip(df_bronze["score"],df_bronze["url"]):
            if 'h' in score_match_bronze :
                match_not_played_yet += f"{match_url} ; "


        to_load = []
        for match_bronze in df_bronze["url"]:
            if (str(match_bronze) in match_list_silver) | (str(match_bronze) in match_not_played_yet) :
                pass
            else:
                to_load.append(match_bronze)



        df = pd.DataFrame(to_load)


        if os.path.exists(match_to_load_filepath):
            os.remove(match_to_load_filepath)

        if not df.empty:
            df.to_csv(match_to_load_filepath, sep=";", index=False, header=False, encoding="utf-8")

        logger.info(f"Matches added : {to_load}")


    # if the file is empty
    else:

        match_not_played_yet = ""
        for score_match_bronze, match_url in zip(df_bronze["score"],df_bronze["url"]):
            if 'h' in score_match_bronze :
                match_not_played_yet += f"{match_url} ; "


        to_load = []
        for match_bronze in df_bronze["url"]:
            if (str(match_bronze) in match_not_played_yet) :
                pass
            else:
                to_load.append(match_bronze)

        logger.info(f"Matches added : {to_load}")
        df = pd.DataFrame(to_load)


        if os.path.exists(match_to_load_filepath):
            os.remove(match_to_load_filepath)

        if not df.empty:
            df.to_csv(match_to_load_filepath, sep=";", index=False, header=False, encoding="utf-8")

