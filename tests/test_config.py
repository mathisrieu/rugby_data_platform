import pytest

from config import ENVIRONMENTS, load_config

PATH_FIELDS = ("TMP_PATH", "LOGS_PATH", "ERRORS_PATH", "BRONZE_PATH", "SILVER_PATH", "GOLD_PATH")


@pytest.mark.parametrize("env", ["DEV", "INT", "AP", "PROD"])
def test_paths_are_scoped_to_environment(env: str):
    config = load_config(env)
    for field in PATH_FIELDS:
        assert env in getattr(config, field).parts, f"{field} n'est pas sous {env}"


def test_environment_is_case_insensitive():
    assert load_config("prod") == load_config("PROD")


def test_defaults_to_dev_without_rugby_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("RUGBY_ENV", raising=False)
    assert load_config() == load_config("DEV")


def test_reads_rugby_env_variable(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("RUGBY_ENV", "AP")
    assert load_config() == load_config("AP")


def test_season_comes_from_environments():
    assert load_config("DEV").SEASON == ENVIRONMENTS["SEASON"]


def test_unknown_environment_fails_loudly():
    with pytest.raises((KeyError, ValueError)):
        load_config("NOPE")
