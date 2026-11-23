
import shutil
from pathlib import Path

import pandas as pd

from src.config import load_config
from src.player_stats.bronze_to_silver.run import run as run_bronze_to_silver


def test_player_stats_bronze_to_silver(tmp_path, monkeypatch):
    # Configuration : les fixtures restent sur le stockage partagé.
    monkeypatch.setenv("RUGBY_DATA_DIR", str(tmp_path))
    fixtures_path = Path(__file__).parent / "fixtures"

    bronze_fixtures = fixtures_path / "bronze" / "player_stats"
    silver_fixtures = fixtures_path / "silver" / "player_stats"

    test_config = load_config("INT")
    test_config.BRONZE_PATH.mkdir(parents=True, exist_ok=True)
    test_config.LOGS_PATH.mkdir(parents=True, exist_ok=True)

    # Copie des données bronze nécessaires au test.
    source = bronze_fixtures
    destination = test_config.BRONZE_PATH / "player_stats"
    shutil.copytree(source, destination, dirs_exist_ok=True)

    # Exécution du traitement.
    run_bronze_to_silver("INT", "top-14", "2026-2027")

    # Comparaison avec le résultat attendu.
    relative_path = Path(
        "player_stats/top-14/2026-2027/bordeaux/maxime-lucu/"
        "maxime-lucu_global_stats.json"
    )

    df_ref = pd.read_json(silver_fixtures / relative_path.relative_to("player_stats"))
    df_tested = pd.read_json(test_config.SILVER_PATH / relative_path)

    assert df_tested.equals(df_ref)

    # Vérification de la suppression des fichiers flag.
    assert not (
        test_config.BRONZE_PATH
        / "player_stats/top-14/2026-2027/bordeaux/maxime-lucu/"
        "maxime-lucu$bordeaux$top-14$2026-2027.flag"
    ).exists()

    assert not (
        test_config.BRONZE_PATH
        / "player_stats/top-14/2026-2027/pau/axel-desperes/"
        "axel-desperes$pau$top-14$2026-2027.flag"
    ).exists()
