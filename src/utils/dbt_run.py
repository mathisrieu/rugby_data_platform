import json
import logging
import subprocess

logger = logging.getLogger(__name__)


def dbt_run(dbt_model: str, dbt_vars: dict) -> None:
    command = [
        "dbt",
        "run",
        "--select",
        dbt_model,
        "--vars",
        json.dumps(dbt_vars),
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )

        logger.info("dbt model '%s' executed successfully", dbt_model)
        logger.debug("dbt output:\n%s", result.stdout)

    except subprocess.CalledProcessError as exc:
        logger.error("Error during execution of dbt model '%s'", dbt_model)
        logger.error("dbt stdout:\n%s", exc.stdout)
        logger.error("dbt stderr:\n%s", exc.stderr)
        raise