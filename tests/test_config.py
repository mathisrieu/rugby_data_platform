
import pytest

from src.config import ENVIRONMENTS, load_config

PATH_FIELDS = (
    "CONTEXT_PATH",
    "TMP_PATH",
    "LOGS_PATH",
    "ERRORS_PATH",
    "BRONZE_PATH",
    "SILVER_PATH",
    "GOLD_PATH",
)


@pytest.fixture
def data_dir(tmp_path, monkeypatch):
    monkeypatch.setenv("RUGBY_DATA_DIR", str(tmp_path))
    return tmp_path


@pytest.mark.parametrize("env", ENVIRONMENTS)
def test_paths_are_scoped_to_environment(env, data_dir):
    config = load_config(env)

    for field in PATH_FIELDS:
        path = getattr(config, field)
        assert env in path.parts
        assert path.is_relative_to(data_dir)


def test_environment_is_case_insensitive(data_dir):
    assert load_config("prod") == load_config("PROD")


def test_defaults_to_dev(data_dir, monkeypatch):
    monkeypatch.delenv("RUGBY_ENV", raising=False)
    assert load_config() == load_config("DEV")


def test_reads_rugby_env_variable(data_dir, monkeypatch):
    monkeypatch.setenv("RUGBY_ENV", "AP")
    assert load_config() == load_config("AP")


def test_season_comes_from_environment_variable(data_dir, monkeypatch):
    monkeypatch.setenv("RUGBY_SEASON", "2027-2028")
    assert load_config().SEASON == "2027-2028"


def test_default_season(data_dir, monkeypatch):
    monkeypatch.delenv("RUGBY_SEASON", raising=False)
    assert load_config().SEASON == "2026-2027"


def test_unknown_environment_fails(data_dir):
    with pytest.raises(ValueError, match="Environnement inconnu"):
        load_config("NOPE")


def test_missing_data_dir_fails(monkeypatch):
    monkeypatch.delenv("RUGBY_DATA_DIR", raising=False)

    with pytest.raises(ValueError, match="RUGBY_DATA_DIR"):
        load_config()
