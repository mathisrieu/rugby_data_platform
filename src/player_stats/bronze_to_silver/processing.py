import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


# def define_player_to_process(BRONZE_PATH:Path):

#     players_to_process = []

#     for team_folder in os.listdir(BRONZE_PATH / Path("player_stats")):

#         if not team_folder.startswith("."):

#             for player_folder in os.listdir(BRONZE_PATH / Path(f"player_stats/{team_folder}")):

#                 player_folder_path = BRONZE_PATH / Path(f"player_stats/{team_folder}/{player_folder}")


#                 flag_file = next(Path(player_folder_path).glob("*.flag"), None)

#                 if flag_file:

#                     player_name, team_name, is_the_first_file, match = flag_file.stem.split("$")

#                     players_to_process.append({
#                         "player_url": player_folder_path.relative_to(BRONZE_PATH),
#                         "player_name": player_name,
#                         "team_name": team_name,
#                         "is_the_first_file": int(is_the_first_file),
#                         "match": match
#                         })
                        
#                     logger.info(f"## Player to process : {player_folder}")




#     return players_to_process



def define_player_to_process(BRONZE_PATH:Path, competition:str, season:str):

    players_to_process = []

    root = BRONZE_PATH / Path(f"player_stats/{competition}/{season}")

    for file_path in root.rglob("*.flag") :

        json_file = next(Path(file_path.parent).glob("*.json"), None)

        players_to_process.append(json_file)

    #     if not team_folder.startswith("."):

    #         for player_folder in os.listdir(BRONZE_PATH / Path(f"player_stats/{team_folder}")):

    #             player_folder_path = BRONZE_PATH / Path(f"player_stats/{team_folder}/{player_folder}")


    #             flag_file = next(Path(player_folder_path).glob("*.flag"), None)

    #             if flag_file:

    #                 player_name, team_name, is_the_first_file, match = flag_file.stem.split("$")

    #                 players_to_process.append({
    #                     "player_url": player_folder_path.relative_to(BRONZE_PATH),
    #                     "player_name": player_name,
    #                     "team_name": team_name,
    #                     "is_the_first_file": int(is_the_first_file),
    #                     "match": match
    #                     })
                        
    #                 logger.info(f"## Player to process : {player_folder}")




    return players_to_process



#print(define_player_to_process("/Volumes/rugby_data/INT/data/bronze"))