import json
import os
from pathlib import Path

from utils.scrapping_config import config_scrap


def scrap_players_per_match(bronze_folder, match, home_team, away_team, competition) -> None:

    url = match

    season = url.replace("https://www.allrugby.com/","").split("/")[0]

    if not os.path.exists(f"{bronze_folder}/players_per_match"):
        os.mkdir(f"{bronze_folder}/players_per_match")


    if not os.path.exists(f"{bronze_folder}/players_per_match/{competition}"):
        os.mkdir(f"{bronze_folder}/players_per_match/{competition}")

    if not os.path.exists(f"{bronze_folder}/players_per_match/{competition}/{season}"):
        os.mkdir(f"{bronze_folder}/players_per_match/{competition}/{season}")


    match = url.split(season)[1].split("matchs/")[1][:-11]

    players_per_match_folder = f"{bronze_folder}/players_per_match/{competition}/{season}/{match}"

    if not os.path.exists(players_per_match_folder):
        os.mkdir(players_per_match_folder)


    soup = config_scrap(url)

    # Cible la table des compositions
    tbody = soup.select_one("#container table tbody")

    players_domicile = []
    players_exterieur = []

    for tr in tbody.find_all("tr"):
        td_right = tr.find("td", class_="txtright")
        td_left  = tr.find("td", class_="txtleft")


        if td_right:
            position = td_right.find_next_sibling().get_text(strip=True)
            link = td_right.find("a", href=lambda h: h and "/joueurs/" in h)
            if link:
                players_domicile.append({"name": link.get_text(strip=True), "url": link.get("href"), "position": position})

        if td_left:
            position = td_left.find_previous_sibling().get_text(strip=True)
            link = td_left.find("a", href=lambda h: h and "/joueurs/" in h)
            if link:
                players_exterieur.append({"name": link.get_text(strip=True), "url": link.get("href"), "position": position})


    if not os.path.exists(players_per_match_folder):
        os.mkdir(players_per_match_folder)


    with open (f"{players_per_match_folder}/{home_team}.json", "w", encoding='utf-8') as f:
        json.dump(players_domicile, f, indent=4, ensure_ascii=False)

    with open (f"{players_per_match_folder}/{away_team}.json", "w", encoding='utf-8') as f:
        json.dump(players_exterieur, f, indent=4, ensure_ascii=False)


    (Path(players_per_match_folder) / "to_do.flag").touch()




#scrap_players_per_match("/Volumes/rugby_data/INT/data/bronze", "https://www.allrugby.com/saison-2026-2027/matchs/gloucester-bordeaux-26867.html", "gloucester", "bordeaux", "champions-cup")