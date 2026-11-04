import locale
import logging
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def transform_calendar (BRONZE_PATH, SILVER_PATH, match_to_add_filepath, competition, season) -> pd.DataFrame :
    bronze_path_calendar = BRONZE_PATH / Path(f"calendar/{competition}/{season}/calendar_bronze.json")
    silver_path_calendar = SILVER_PATH / Path(f"calendar/{competition}/{season}/calendar_silver.json")

    df = pd.read_json(bronze_path_calendar)

    if df.empty:
            sys.exit()

    df_match_to_add = pd.read_csv(match_to_add_filepath, sep=';', header=None, names=["url"])


    if silver_path_calendar.exists():

        df_silver = pd.read_json(silver_path_calendar, dtype={"date":str,"score_equipe_domicile":str,"score_equipe_exterieur":str,"is_loaded":bool})

    else:

        silver_path_calendar.touch()
        df_silver = pd.DataFrame()


    if not df_silver.empty:

        df = df[df["url"].isin(df_match_to_add["url"])]

        df_silver["date"] = pd.to_datetime(df_silver["date"], format="%Y-%m-%d")
        df_silver["date"] = df_silver["date"].dt.strftime("%d-%m-%Y")


    # colonne journee

    df["journee"] = df["journee"].str.lower()
    df["journee"] = df["journee"].str.replace(" ", "-")


    # colonne date

    locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")

    dates = df["date"]

    new_dates = []
    for date in dates:
        date1 = date.replace("1er","1")
        date_obj = datetime.strptime(date1, "%A %d %B %Y")
        new_format = date_obj.strftime("%d-%m-%Y")
        new_dates.append(new_format)


    df["date"] = new_dates



    # colonne equipe domicile

    df["equipe_domicile"] = df["equipe_domicile"].str.lower()
    df["equipe_domicile"] = df["equipe_domicile"].str.replace(" ", "-")


    # colonne equipe exterieur

    df["equipe_exterieur"] = df["equipe_exterieur"].str.lower()
    df["equipe_exterieur"] = df["equipe_exterieur"].str.replace(" ", "-")


    # colonne home score

    df["score_equipe_domicile"] = df["score"].str.split(" - ").str[0]


    # colonne away score

    df["score_equipe_exterieur"] = df["score"].str.split(" - ").str[1]


    # colonne result

    df["result"] = df["gagnant"].str.lower()


    #colonne url match

    url_root = "https://www.allrugby.com"

    urls = df["url"]
    new_urls = []

    for url in urls:

        new_urls.append(f"{url_root}{url}")

    df["match_url"] = new_urls



    #suppression colonnes

    df = df.drop(columns=["score", "gagnant", "url"])


    # calcul du resullat du match

    home_scores = df["score_equipe_domicile"]
    away_scores = df["score_equipe_exterieur"]
    home_teams = df["equipe_domicile"]
    away_teams = df["equipe_exterieur"]


    new_home_scores = []
    new_away_scores = []
    new_results = []

    for home_score, away_score, home_team, away_team in zip(home_scores, away_scores, home_teams, away_teams):
        if "h" in home_score or "en cours" in home_score:
            new_home_scores.append(None)
            new_away_scores.append(None)
            new_results.append(None)
        elif home_score == away_score:
            new_home_scores.append(home_score)
            new_away_scores.append(away_score)
            new_results.append("draw")
        else:
            new_home_scores.append(home_score)
            new_away_scores.append(away_score)
            if max(home_score,away_score) == home_score:
                new_results.append(home_team)
            else:
                new_results.append(away_team)


    df["score_equipe_domicile"] = new_home_scores
    df["score_equipe_exterieur"] = new_away_scores
    df["result"] = new_results


    df = df[df["result"].notna() & (df["result"].str.strip() != "")]

    df["is_loaded"] = False

    df_data = pd.concat([df_silver,df], ignore_index=True)


    return df_data


#print(transform_calendar("/Volumes/rugby_data/INT/data/bronze", "/Volumes/rugby_data/INT/data/silver", "/Volumes/rugby_data/INT/tmp/match_to_add_champions-cup.csv", "champions-cup", "2026-2027"))