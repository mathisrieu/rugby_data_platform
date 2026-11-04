import json
import os
import unicodedata
from pathlib import Path

import pandas as pd


def _normaliser_texte(value: str) -> str:
    value = unicodedata.normalize("NFKD", str(value))
    return "".join(
        character for character in value if not unicodedata.combining(character)
    ).lower().strip()



def _split_name(name: str) -> tuple[str, str]:
        first_parts = []
        last_parts = []
        for item in name.split(" "):
            if item.isupper():
                last_parts.append(item)
            else:
                first_parts.append(item)
        return " ".join(first_parts), " ".join(last_parts)



def _trouver_rugbypass_id(row, liste_des_joueurs):
    # retrieve first name and last name of current row
    prenom = _normaliser_texte(row["first_name"])
    nom = _normaliser_texte(row["last_name"])

    # cleaning (replace space by '-')
    prenom_nettoye = prenom.replace(" ", "-")
    nom_nettoye = nom.replace(" ", "-")

    # Strat 1 : we look if the first name AND the last name are both contained i the ID
    # Example : 'romain' in 'romain-ntamack' AND 'ntamack' in 'romain-ntamack'
    for player in liste_des_joueurs:
        player_normalise = _normaliser_texte(player)
        if nom_nettoye in player_normalise and prenom_nettoye in player_normalise:
            return player

    # Strat 2 (for security) : If the first name do not match (i.e : different spelling), we only look for the last name in order to not have an empty value
    for player in liste_des_joueurs:
        if nom_nettoye in _normaliser_texte(player):
            return player

    return None  # No player finded



def _trouver_rugbypass_url(player_name, players):
        for player in players:
            if player["player_name"] == player_name:
                player_url = player["player_url"]

                return player_url




def transform_players_per_match(match_folder, BRONZE_PATH, SILVER_PATH) -> None:


    team_roster_path = SILVER_PATH / 'teams/teams_rosters.json'

    match_folder = match_folder.relative_to(BRONZE_PATH)

    match_folder_bronze = BRONZE_PATH / match_folder
    match_folder_silver = SILVER_PATH / match_folder
    

    os.makedirs(match_folder_silver, exist_ok=True)

    (Path(match_folder_silver) / "to_do.flag").touch()

    files = list(Path(match_folder_bronze).glob("*.json"))


    for file in files:

        team_name = file.stem

        silver_filepath = f"{match_folder_silver}/{team_name}.json"

        df = pd.read_json(file)


        df[["first_name", "last_name"]] = df["name"].apply(
            lambda name: pd.Series(_split_name(name))
        )

        #delting columns
        df = df.drop(columns=["name"])


        # Mapping with team roster file, in order to retrieve the player name as it is required by rugbypass

        df_team_roster = pd.read_json(team_roster_path)

        players = df_team_roster.loc[df_team_roster["team"] == team_name, "players"].values[0]

        players_list = [p["player_name"] for p in players]

        df["rugbypass_player_id"] = df.apply(
            lambda row, players_list=players_list: _trouver_rugbypass_id(row, players_list), axis=1
        )

        # Fallback: URL contains rugbypass id when the mapping with name fail
        url_player_ids = (
            df["url"]
            .str.split("/joueurs/").str[1]
            .str.rsplit("-", n=1).str[0]
        )
        df["rugbypass_player_id"] = df["rugbypass_player_id"].fillna(url_player_ids)


        #add the rugbypass_player_url

        df["rugbypass_player_url"] = df.apply(
            lambda row, players=players: _trouver_rugbypass_url(row["rugbypass_player_id"], players), axis=1
        )




        data = df.to_json(orient="records", force_ascii=False)


        json_data = json.loads(data)


        if json_data:

            with open (silver_filepath, "w", encoding="utf-8") as f:
                json.dump(json_data, f, indent=4, ensure_ascii=False)


