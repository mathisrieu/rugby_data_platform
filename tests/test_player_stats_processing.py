from pathlib import Path

from src.player_stats.raw_to_bronze.processing import define_matches_to_process


def test_matches_to_process_is_scoped_to_competition_and_season(tmp_path: Path):
    target_match = (
        tmp_path
        / "players_per_match"
        / "top-14"
        / "saison-2025-2026"
        / "bordeaux-toulouse"
    )
    other_competition_match = (
        tmp_path
        / "players_per_match"
        / "pro-d2"
        / "saison-2025-2026"
        / "oyonnax-grenoble"
    )
    other_season_match = (
        tmp_path
        / "players_per_match"
        / "top-14"
        / "saison-2024-2025"
        / "bordeaux-toulouse"
    )

    for match_folder in (
        target_match,
        other_competition_match,
        other_season_match,
    ):
        match_folder.mkdir(parents=True)
        (match_folder / "to_do.flag").touch()

    assert define_matches_to_process(tmp_path, "top-14", "2025-2026") == [
        target_match
    ]
