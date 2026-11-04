import csv


def write_error_file(player, team_name, player_url, competition, competition_name, season, error_message, ERRORS_PATH):
    
    header = ['player_name','team_name','player_url', 'competition', 'competition_name', 'season', 'error']
    error = [str(player), str(team_name), player_url, competition, competition_name, season, str(error_message)]

    scrap_error_file_path = ERRORS_PATH / "scrapping_errors.csv"
    scrap_error_file_path.parent.mkdir(parents=True, exist_ok=True)

    file_exists = scrap_error_file_path.exists()

    with open(scrap_error_file_path,'a', newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(header)
        writer.writerow(error)