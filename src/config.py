import os
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path("/Volumes/rugby_data/")

ENVIRONMENTS = {
    "PROD": {
        "CONTEXT_PATH": PROJECT_ROOT / "PROD/context",
        "TMP_PATH": PROJECT_ROOT / "PROD/tmp",
        "LOGS_PATH": PROJECT_ROOT / "PROD/logs",
        "ERRORS_PATH": PROJECT_ROOT / "PROD/errors",
        "BRONZE_PATH": PROJECT_ROOT / "PROD/data/bronze",
        "SILVER_PATH": PROJECT_ROOT / "PROD/data/silver",
        "GOLD_PATH": PROJECT_ROOT / "PROD/data/gold",
    },
    "AP": {
        "CONTEXT_PATH": PROJECT_ROOT / "AP/context",
        "TMP_PATH": PROJECT_ROOT / "AP/tmp",
        "LOGS_PATH": PROJECT_ROOT / "AP/logs",
        "ERRORS_PATH": PROJECT_ROOT / "AP/errors",
        "BRONZE_PATH": PROJECT_ROOT / "AP/data/bronze",
        "SILVER_PATH": PROJECT_ROOT / "AP/data/silver",
        "GOLD_PATH": PROJECT_ROOT / "AP/data/gold",
    },
    "INT": {
        "CONTEXT_PATH": PROJECT_ROOT / "INT/context",
        "TMP_PATH": PROJECT_ROOT / "INT/tmp",
        "LOGS_PATH": PROJECT_ROOT / "INT/logs",
        "ERRORS_PATH": PROJECT_ROOT / "INT/errors",
        "BRONZE_PATH": PROJECT_ROOT / "INT/data/bronze",
        "SILVER_PATH": PROJECT_ROOT / "INT/data/silver",
        "GOLD_PATH": PROJECT_ROOT / "INT/data/gold",
        },
    "DEV": {
        "CONTEXT_PATH": PROJECT_ROOT / "DEV/context",
        "TMP_PATH": PROJECT_ROOT / "DEV/tmp",
        "LOGS_PATH": PROJECT_ROOT / "DEV/logs",
        "ERRORS_PATH": PROJECT_ROOT / "DEV/errors",
        "BRONZE_PATH": PROJECT_ROOT / "DEV/data/bronze",
        "SILVER_PATH": PROJECT_ROOT / "DEV/data/silver",
        "GOLD_PATH": PROJECT_ROOT / "DEV/data/gold",
    },

    "SEASON":"2026-2027",
}

CURRENT_ENV = os.getenv("RUGBY_ENV", "DEV").upper()
CONFIG = ENVIRONMENTS[CURRENT_ENV]


@dataclass (frozen=True)
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
    """Retourne les chemins de l'environnement demandé.

    L'environnement peut être fourni directement ou via RUGBY_ENV.
    DEV est utilisé par défaut.
    """
    selected_environment = (environment or os.getenv("RUGBY_ENV", "DEV")).upper()

    config = Config(
        CONTEXT_PATH= ENVIRONMENTS[selected_environment].get("CONTEXT_PATH"),
        TMP_PATH= ENVIRONMENTS[selected_environment].get("TMP_PATH"),
        LOGS_PATH= ENVIRONMENTS[selected_environment].get("LOGS_PATH"),
        ERRORS_PATH= ENVIRONMENTS[selected_environment].get("ERRORS_PATH"),
        BRONZE_PATH= ENVIRONMENTS[selected_environment].get("BRONZE_PATH"),
        SILVER_PATH= ENVIRONMENTS[selected_environment].get("SILVER_PATH"),
        GOLD_PATH= ENVIRONMENTS[selected_environment].get("GOLD_PATH"),
        SEASON= ENVIRONMENTS.get("SEASON")
    )

    
    try:
        return config
    except KeyError as error:
        available_environments = ", ".join(ENVIRONMENTS)
        raise ValueError(
            f"Environnement inconnu: {selected_environment!r}. "
            f"Valeurs acceptées: {available_environments}"
        ) from error




