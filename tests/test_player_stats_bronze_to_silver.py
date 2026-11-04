import shutil
from pathlib import Path
import pandas as pd

from src.player_stats.bronze_to_silver.run import run as run_bronze_to_silver


def test_player_stats_bronze_to_silver ():

    test_folder_path = Path("/Volumes/rugby_data/INT/tests/bronze/player_stats")
    data_folder_path = Path("/Volumes/rugby_data/INT/data/bronze/player_stats")

    shutil.copytree(test_folder_path, data_folder_path, dirs_exist_ok=True)

    run_bronze_to_silver("INT", "top-14", "2026-2027")

    df_ref = pd.read_json("/Volumes/rugby_data/INT/tests/silver/player_stats/top-14/2026-2027/bordeaux/maxime-lucu/maxime-lucu_global_stats.json")
    df_tested = pd.read_json("/Volumes/rugby_data/INT/data/silver/player_stats/top-14/2026-2027/bordeaux/maxime-lucu/maxime-lucu_global_stats.json")

    assert df_tested.equals(df_ref)

    assert not Path("/Volumes/rugby_data/INT/data/bronze/player_stats/top-14/2026-2027/bordeaux/maxime-lucu/maxime-lucu$bordeaux$top-14$2026-2027.flag").exists()
    assert not Path("/Volumes/rugby_data/INT/data/bronze/player_stats/top-14/2026-2027/pau/axel-desperes/axel-desperes$pau$top-14$2026-2027.flag").exists()
