from importlib import import_module
from typing import Any


def run_project_task(module_path: str, *args: str) -> Any:
    task_module = import_module(module_path)
    return task_module.run(*args)
