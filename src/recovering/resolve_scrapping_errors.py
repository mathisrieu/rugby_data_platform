import pandas as pd
import json
from pathlib import Path
from src.recovering.scrapping_functions import find_player_url


def resolve_scrapping_errors(ERRORS_FOLDER:Path, SILVER_PATH:Path):

    df = pd.read_csv(ERRORS_FOLDER / "scrapping_errors.csv", delimiter=',')

    players = df[["player_name","team_name"]].drop_duplicates().values.tolist()

    with open (SILVER_PATH / "teams/teams_rosters.json", "r", encoding='utf-8') as f:
        team_rosters = json.load(f)

    wrong_urls = []

    for player in players :

        player_name = player[0]
        team_name = player[1]

        player_url = find_player_url(player_name)

        if player_url is not None :
            for team in team_rosters :
                if team["team"]==player[1]:
                    team["players"].append(
                        {
                        "player_name": str(player_name),
                        "player_url": str(player_url)
                        }
                    )
        else :
            wrong_urls.append([player_name, team_name])

    with open (SILVER_PATH / "teams/teams_rosters.json", "w", encoding='utf-8') as f:
        json.dump(team_rosters, f, indent=4, ensure_ascii=True)

    with open (ERRORS_FOLDER / "wrong_urls.json", "w", encoding='utf-8') as f:
        json.dump(wrong_urls, f, indent=4, ensure_ascii=True)