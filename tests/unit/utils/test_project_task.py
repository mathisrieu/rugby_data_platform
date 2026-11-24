
from unittest.mock import MagicMock, patch

from src.utils.project_task import main, run_project_task


def test_run_project_task_imports_module_and_calls_run():
    fake_module = MagicMock()
    fake_module.run.return_value = None

    with patch(
        "src.utils.project_task.import_module",
        return_value=fake_module,
    ) as mock_import:
        run_project_task(
            "src.player_stats.raw_to_bronze.run",
            "DEV",
            "top-14",
            "2026-2027",
        )

    mock_import.assert_called_once_with(
        "src.player_stats.raw_to_bronze.run",
    )
    fake_module.run.assert_called_once_with(
        "DEV",
        "top-14",
        "2026-2027",
    )



def test_main_parses_arguments_and_calls_run_project_task():
    with (
        patch(
            "src.utils.project_task.run_project_task"
        ) as mock_run,
        patch(
            "sys.argv",
            [
                "project_task.py",
                "src.player_stats.raw_to_bronze.run",
                "DEV",
                "top-14",
                "2026-2027",
            ],
        ),
    ):
        main()

    mock_run.assert_called_once_with(
        "src.player_stats.raw_to_bronze.run",
        "DEV",
        "top-14",
        "2026-2027",
    )