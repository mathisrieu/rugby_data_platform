import logging
from datetime import datetime
from pathlib import Path

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# -------------- Logging configuration ----------------------

def setup_logging(log_path: Path, script_dir: Path) -> None:

    script_folder = script_dir.parent.name

    (log_path / script_folder).mkdir(parents=True, exist_ok=True)

    script_file = script_dir.name

    logging.basicConfig(
        filename = log_path / script_folder / Path(f"{script_file}_{timestamp}.log"),
        filemode = 'w',
        format = f"%(asctime)s - %(levelname)s - {script_folder}.{script_file}.%(module)s  - %(message)s",
        datefmt = '%Y-%m-%d %H:%M:%S',
        level = logging.INFO
    )




# from src.utils.logging import setup_logging

#     # -------------- Logging configuration ----------------------
#     setup_logging(config.LOGS_PATH)
#     logger = logging.getLogger(__name__)