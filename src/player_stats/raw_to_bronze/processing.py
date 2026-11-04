import json
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


# def define_matches_to_process(SILVER_PATH) -> list:

#     matches_to_process = []

#     for season_folder in os.listdir(SILVER_PATH / "players_per_match"):

#         if not season_folder.startswith("."):

#             for match in os.listdir(SILVER_PATH / f"players_per_match/{season_folder}"):

#                 match_folder_path = SILVER_PATH / f"players_per_match/{season_folder}/{match}"

#                 flag_file = f"{match_folder_path}/to_do.flag"

#                 if os.path.exists(flag_file):

#                     matches_to_process.append(match_folder_path)
#                     logger.info(f"## Match to process : {match}")


#     return matches_to_process

def define_matches_to_process(SILVER_PATH) -> list:

    matches_to_process = []

    root = SILVER_PATH / "players_per_match"

    for file_path in root.rglob("*.flag") :

        # json_file = next(Path(file_path.parent).glob("*.json"), None)
        # matches_to_process.append(match_folder_path)

        matches_to_process.append(file_path.parent)
        logger.info(f"## Match to process : {file_path.parent}")


    return matches_to_process




def define_players_to_process(match_folder_path, SILVER_PATH):

    players_to_process = []

    for team in os.listdir(match_folder_path):

        if team.endswith(".json"):

            team_filepath = f"{match_folder_path}/{team}"

            with open(team_filepath, "r", encoding="utf-8") as f:

                data = json.load(f)

                team_name = team.replace(".json","")
                logger.info(f"#### Team to process : {team_name}")

                for player_dict in data:
                    player = player_dict.get("rugbypass_player_id")
                    player_url = player_dict.get("rugbypass_player_url")

                                    
                    logger.info(f"###### Player to process : {player}")

                    # if not Path(SILVER_PATH / f"player_stats/{team_name}/{player}/{player}_global_stats.json").is_file():
                    #     is_the_first_file = 1
                    # else:
                    #     is_the_first_file = 0

                    players_to_process.append({
                        "player_name": player,
                        "team_name": team_name,
                        #"is_the_first_file": is_the_first_file,
                        "player_url": player_url,
                    })

    return players_to_process



def update_calendar(SILVER_PATH:Path, match_folder:str, competition:str, season:str) :

    calendar_path = SILVER_PATH / Path(f"calendar/{competition}/{season}/calendar_silver.json")

    with open (calendar_path, "r", encoding='utf-8') as f:
        matches = json.load(f)

    for match in matches :
        if  match_folder in match["match_url"] :
            match["is_loaded"] = True

    with open (calendar_path, "w", encoding='utf-8') as f:
        json.dump(matches, f, indent=4, ensure_ascii=False)




