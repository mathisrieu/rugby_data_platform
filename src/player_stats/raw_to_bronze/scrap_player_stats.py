
# extraction script
# source -> bronze

import json
import logging
import os
from pathlib import Path

from utils.scrapping_config import config_scrap

logger = logging.getLogger(__name__)


def scrap_player_stats(player_name:str, team_name:str, player_url:str, competition:str, competition_name:str, season:str, BRONZE_PATH:Path):


    bronze_folder = BRONZE_PATH / "player_stats"

    if not os.path.exists(bronze_folder):
        os.mkdir(bronze_folder)

    if not os.path.exists(f"{bronze_folder}/{competition}"):
        os.mkdir(f"{bronze_folder}/{competition}")

    if not os.path.exists(f"{bronze_folder}/{competition}/{season}"):
        os.mkdir(f"{bronze_folder}/{competition}/{season}")

    if not os.path.exists(f"{bronze_folder}/{competition}/{season}/{team_name}"):
        os.mkdir(f"{bronze_folder}/{competition}/{season}/{team_name}")

    if not os.path.exists(f"{bronze_folder}/{competition}/{season}/{team_name}/{player_name}"):
        os.mkdir(f"{bronze_folder}/{competition}/{season}/{team_name}/{player_name}")

    # if not os.path.exists(f"{bronze_folder}/{competition}/{season.replace("/","-")}/{team_name}/{player_name}/archive"):
    #     os.mkdir(f"{bronze_folder}/{competition}/{season.replace("/","-")}/{team_name}/{player_name}/archive")



    path_stats = f"{bronze_folder}/{competition}/{season}/{team_name}/{player_name}/{player_name}_global_stats.json"


    soup = config_scrap(player_url)


    stats_element = soup.select_one("#app-comp-stats")


    if stats_element:
        # Retrieve raw text from <div>
        json_raw = stats_element.get_text(strip=True)
        
        try:
            # Convert raw string into a Dict
            data_json = json.loads(json_raw)
            stats_complet = None

            # Look for the complete stats element for competition
            for item in data_json:
                if (item.get("competition", {}).get("name") == competition_name) & (item.get("competition", {}).get("season", {}).get("label") == season.replace("-","/")) :
                    stats_complet = item
                    stats_complet["player_url"] = player_url
                    break

            if stats_complet:
                #archive latest global_stats file
                # if is_the_first_file == 0:
                #     source = Path(path_stats)
                #     destination = Path(f"{bronze_folder}/{team_name}/{player_name}/archive/{player_name}_global_stats.json")
                #     source.rename(destination)

                # Save all stats into json file
                with open(path_stats, "w", encoding="utf-8") as f:
                    json.dump(stats_complet, f, indent=4, ensure_ascii=False)



                flag_filepath = Path(f"{bronze_folder}/{competition}/{season}/{team_name}/{player_name}/{player_name}${team_name}${competition}${season}.flag")
                flag_filepath.touch()


                
                
            

        except json.JSONDecodeError:
            logger.exception("Erreur de décodage : Le flux HTML récupéré est incomplet ou mal formé.")
    else:
        raise RuntimeError("La balise #app-comp-stats est introuvable sur la page.")



#scrap_player_stats("maxime-lucu", "bordeaux", "https://www.rugbypass.com/players/maxime-lucu/", "champions-cup", "Investec Champions Cup", "2026-2027", Path("/Volumes/rugby_data/INT/data/bronze"))