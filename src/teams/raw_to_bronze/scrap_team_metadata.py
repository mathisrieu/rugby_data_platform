from bs4 import BeautifulSoup
from pathlib import Path
import csv


def scrap_team_metadata(BRONZE_PATH: Path, team, soup: BeautifulSoup):

    # retrieve team logo
    logo_tag = soup.select_one("img.team-logo")

    team_logo = logo_tag.get("data-srcset").split("maxw=")[0] if logo_tag else None

    
    # retrieve team color
    color_tag = soup.select_one("body > main > style")

    team_color = (
        color_tag.get_text()
        .split("background-color:")[1]
        .split(";")[0]
        .strip()
    ) if color_tag else None


    metadata_filepath = BRONZE_PATH / "teams/metadata/teams_metadata.csv"
    metadata_filepath.parent.mkdir(parents=True, exist_ok=True)

    if not metadata_filepath.exists():
        with metadata_filepath.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["team", "color", "logo"])

    with metadata_filepath.open("r", newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f, delimiter=";"))

    with metadata_filepath.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")

        for row in rows:
            if not row or row[0] != team:
                writer.writerow(row)

        writer.writerow([team, team_color, team_logo])


