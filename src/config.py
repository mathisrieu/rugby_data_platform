
import os
from dataclasses import dataclass
from pathlib import Path

ENVIRONMENTS = ("DEV", "INT", "AP", "PROD")
DEFAULT_SEASON = "2026-2027"


@dataclass(frozen=True)
class Config:
    CONTEXT_PATH: Path
    TMP_PATH: Path
    LOGS_PATH: Path
    ERRORS_PATH: Path
    BRONZE_PATH: Path
    SILVER_PATH: Path
    GOLD_PATH: Path
    SEASON: str


def load_config(environment: str | None = None) -> Config:
    """Charge les chemins de stockage pour l'environnement demandé.

    RUGBY_DATA_DIR désigne la racine du stockage partagé,
    par exemple le point de montage Azure File Share.
    """
    selected_environment = (
        environment or os.getenv("RUGBY_ENV", "DEV")
    ).upper()

    if selected_environment not in ENVIRONMENTS:
        available = ", ".join(ENVIRONMENTS)
        raise ValueError(
            f"Environnement inconnu : {selected_environment!r}. "
            f"Valeurs acceptées : {available}"
        )

    data_dir = os.getenv("RUGBY_DATA_DIR")
    if not data_dir:
        raise ValueError(
            "La variable d'environnement RUGBY_DATA_DIR doit être définie."
        )

    root = Path(data_dir).expanduser().resolve()
    env_root = root / selected_environment
    data_root = env_root / "data"

    return Config(
        CONTEXT_PATH=env_root / "context",
        TMP_PATH=env_root / "tmp",
        LOGS_PATH=env_root / "logs",
        ERRORS_PATH=env_root / "errors",
        BRONZE_PATH=data_root / "bronze",
        SILVER_PATH=data_root / "silver",
        GOLD_PATH=data_root / "gold",
        SEASON=os.getenv("RUGBY_SEASON", DEFAULT_SEASON),
    )
