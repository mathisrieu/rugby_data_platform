
from src.utils.scrapping_config import config_scrap

def find_player_url(player_name) -> str:

    url_root = "https://www.rugbypass.com/players"

    player_url = f"{url_root}/{player_name}"

    try :
        soup = config_scrap(player_url)
    except Exception as error :
        print(error)
        if error.response is not None and error.response.status_code == 404:
            print("URL not found : ", player_url)
            return None
        else :
            print("URL error : ", error)
            return None

    # if not soup.get_text(strip=True):
    #     print("erreur (page vide): ", player_url)
    #     return None
    # else :
    #     #print("url OK : ", player_url)
    #     return player_url


    message404 = soup.select_one("body > main > div > div")
    if message404:
        message = message404.get_text(strip=True)
        if message == "message-404":
            return None
        
    return player_url
