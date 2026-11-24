
import argparse
from importlib import import_module
from typing import Any


def run_project_task(module_path: str, *args: str) -> Any:
    """Import and execute an ETL task."""
    task_module = import_module(module_path)
    return task_module.run(*args)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Execute an ETL task.",
    )
    parser.add_argument("module_path")
    parser.add_argument("env")
    parser.add_argument("competition")
    parser.add_argument("season")

    args = parser.parse_args()

    run_project_task(
        args.module_path,
        args.env,
        args.competition,
        args.season,
    )


if __name__ == "__main__":
    main()
