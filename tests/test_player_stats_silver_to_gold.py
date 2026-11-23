
import shutil

import pandas as pd

from src.config import load_config
from src.player_stats.silver_to_gold.run import run as run_silver_to_gold


def test_player_stats_silver_to_gold():
    config = load_config("INT")

    test_path = config.CONTEXT_PATH.parent / "tests"
    silver_fixtures = test_path / "silver" / "player_stats"
    gold_fixtures = test_path / "gold" / "player_stats"

    silver_data = config.SILVER_PATH / "player_stats"

    # Préparation des données Silver.
    shutil.copytree(silver_fixtures, silver_data, dirs_exist_ok=True)

    # Exécution du pipeline Silver -> Gold.
    run_silver_to_gold("INT", "top-14", "2026-2027")

    # Comparaison du résultat Gold avec la référence.
    output_file = config.GOLD_PATH / "player_stats" / "top-14_2026-2027.parquet"
    reference_file = gold_fixtures / "top-14_2026-2027.parquet"

    df_ref = pd.read_parquet(reference_file)
    df_tested = pd.read_parquet(output_file)

    assert df_tested.equals(df_ref)
