import os
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from src.teams.raw_to_bronze.scrap_team_metadata import scrap_team_metadata


def scrap_team_roster(BRONZE_PATH:Path, team) -> None:

    url = f"https://www.rugbypass.com/teams/{team}/"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")


    #retrieve team metadata

    scrap_team_metadata(BRONZE_PATH, team, soup)
    return

    # retrieve players list

    players_div = soup.select_one(".team-players-list")

    if not players_div:
        print(f"Balise '.team-players-list' introuvable pour {team}, skip.")
        sys.exit(1)

    os.makedirs(BRONZE_PATH / "teams", exist_ok=True)

    html_path = BRONZE_PATH / "teams" / f"{team}.html"


    with open(html_path, "w", encoding="utf-8") as f:
        f.write(str(players_div))


    

    #print(f"HTML file saved at {html_path}")

scrap_team_roster(Path("/Volumes/rugby_data/DEV/data"), "bordeaux")