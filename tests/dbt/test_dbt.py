import shutil
import subprocess

import pytest


def test_dbt_project_exposes_only_gold_model():
    """Ensure the expected Gold model is the only discovered model."""
    if shutil.which("dbt") is None:
        pytest.skip("dbt is not installed in this environment")

    result = subprocess.run(
        [
            "dbt",
            "ls",
            "--project-dir",
            ".",
            "--profiles-dir",
            "dbt",
            "--resource-type",
            "model",
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    models = {
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip().startswith("rugby_data.")
    }

    assert models == {"rugby_data.gold.dbt-competition-stats"}