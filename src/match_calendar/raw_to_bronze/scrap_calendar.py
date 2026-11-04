from utils.scrapping_config import config_scrap


def scrap_calendar(competition):

    url = f"https://www.allrugby.com/competitions/{competition}/calendrier.html"

    soup = config_scrap(url)

    calendrier = soup.select_one("#container > div > div.calendrier")

    matches = []
    current_journee = None
    current_date = None

    for journee_div in calendrier.find_all("div", class_="journee"):

        titre = journee_div.find("div", class_="titre")
        if titre:
            current_journee = titre.get_text(strip=True)

        ul_matchs = journee_div.find("ul", class_="matchs")

        if not ul_matchs:
            continue

        for element in ul_matchs.children:
            if not hasattr(element, "get"):
                continue

            if "sep_dat" in element.get("class", []):
                current_date = element.get_text(strip=True)
                continue

            lien = element.find("a", class_="mat")
            if not lien:
                continue

            logs = lien.find_all("div", class_="log")
            res  = lien.find("div", class_="res")

            if len(logs) < 2 or not res:
                continue

            equipe_domicile  = logs[0].get_text(strip=True)
            equipe_exterieur = logs[1].get_text(strip=True)
            score            = res.get_text(strip=True)
            url_match        = lien.get("href", "")


            gagnant = lien.find("b")
            gagnant = gagnant.get_text(strip=True) if gagnant else "nul"

            matches.append({
                "journee":          current_journee,
                "date":             current_date,
                "equipe_domicile":  equipe_domicile,
                "equipe_exterieur": equipe_exterieur,
                "score":            score,
                "gagnant":          gagnant,
                "url":              url_match,
            })

    return matches



