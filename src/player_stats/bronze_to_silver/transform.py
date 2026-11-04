import json
import logging
from pathlib import Path

#import pandas as pd



logger = logging.getLogger(__name__)

def clean_json(json_path:Path, BRONZE_PATH:Path, SILVER_PATH:Path) -> None:

    with open (json_path, "r", encoding='utf-8') as f:
        data = json.load(f)

    #cleaning json dict
    del data["main"]
    del data["group"]

    #cleaning competition dict
    competition_keys_to_delete = ["oid", "ovid", "logo", "logoCircle", "epoch"]
    for key in competition_keys_to_delete :
        del data["competition"][key]

    #cleaning season dict
    data["competition"]["season"] = data["competition"]["season"]["label"]

    #cleaning stats dict
    data["team_id"] = data["competition"]["stats"]["stats"]["teamId"]

    del data["competition"]["stats"]["stats"]["teamId"]

    data["competition"]["stats"] = data["competition"]["stats"]["stats"]

    

    with open(SILVER_PATH / json_path.relative_to(BRONZE_PATH), "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)




#clean_json(Path("/Volumes/rugby_data/INT/data/bronze/player_stats/Investec Champions Cup/2026-2027/bordeaux/maxime-lucu/maxime-lucu_global_stats.json"), Path("/Volumes/rugby_data/INT/data/bronze"), Path("/Volumes/rugby_data/INT/data/silver"))