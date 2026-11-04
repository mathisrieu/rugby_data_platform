import json
import os
from pathlib import Path

from bs4 import BeautifulSoup


def write_teams_rosters_file(bronze_folder_root, silver_folder_root) -> None :


    team_folder = "/teams"

    # Création du dossier team s'il n'existe pas dans le dossier silver
    os.makedirs(f"{silver_folder_root}{team_folder}", exist_ok=True)

    # Initialization of the team_rosters file
    with open(f"{silver_folder_root}{team_folder}/teams_rosters.json","w",encoding="utf-8") as f:
        f.write("[\n")

    counter = 0
    nb_file = len(list(Path(f"{bronze_folder_root}{team_folder}").glob("*.html")))


    for file in Path(f"{bronze_folder_root}{team_folder}").rglob("*.html"):

        counter += 1  # noqa: SIM113

        team = file.name.replace(".html","")

        with open(file, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")


        player_list = []

        # For each player :
        for player_box in soup.find_all("div", class_="player-item"):

            # retrieve player name from <div class="title">
            player_name = player_box.find("div", class_="title")
            player_name = player_name.text.strip().lower().replace(" ", "-") if player_name else None

            # retrieve player url from <a> tag
            a_tag = player_box.find("a", class_="link-box")
            player_url = a_tag["href"] if a_tag and "href" in a_tag.attrs else None

            player_list.append(
                {
                "player_name":player_name,
                "player_url":player_url
                }
            )


        data = {
            "team":team,
            "players":player_list
        }

        with open(f"{silver_folder_root}{team_folder}/teams_rosters.json","a",encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            if(counter < nb_file):
                f.write(",\n")


    with open(f"{silver_folder_root}{team_folder}/teams_rosters.json","a",encoding="utf-8") as f:
        f.write("]\n")



