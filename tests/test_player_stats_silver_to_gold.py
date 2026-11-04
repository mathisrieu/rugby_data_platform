import shutil
from pathlib import Path
import pandas as pd

from src.player_stats.silver_to_gold.run import run as run_silver_to_gold


def test_player_stats_silver_to_gold():

    test_folder_path = Path("/Volumes/rugby_data/INT/tests/silver/player_stats")
    data_folder_path = Path("/Volumes/rugby_data/INT/data/silver/player_stats")

    shutil.copytree(test_folder_path, data_folder_path, dirs_exist_ok=True)

    run_silver_to_gold("INT", "top-14", "2026-2027")

    df_ref = pd.read_parquet("/Volumes/rugby_data/INT/tests/gold/player_stats/top-14_2026-2027.parquet")
    df_tested = pd.read_parquet("/Volumes/rugby_data/INT/data/gold/player_stats/top-14_2026-2027.parquet")

    assert df_tested.equals(df_ref)


test_player_stats_silver_to_gold()

