from bs4 import BeautifulSoup
import requests
from DatabaseConnection import DatabaseConnector
from app import get_user_name_and_school   

def split_name(full_name):
    parts = full_name.strip().split()
    if len(parts) == 0:
        return None, None
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], " ".join(parts[1:])

def scrape_player():
    target_first, target_last, school = get_user_name_and_school()

    if target_first is None:
        print("No name entered.")
        return None

    url = "https://gomountaineers.com/sports/womens-volleyball/roster"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    players = soup.select(".sidearm-roster-player")

    db = DatabaseConnector("player_identifying_information.db")
    db.connect()

    for p in players:
        name_tag = p.select_one(".sidearm-roster-player-name")
        hometown_tag = p.select_one(".sidearm-roster-player-hometown")
        eligibility_tag = p.select_one(".sidearm-roster-player-academic-year")
        position_tag = p.select_one(".sidearm-roster-player-position-long-short")
        height_tag = p.select_one(".sidearm-roster-player-height")

        if not name_tag:
            continue

        raw_name = name_tag.get_text(strip=True)
        raw_name = raw_name.lstrip("0123456789 ").strip()

        first, last = split_name(raw_name)

        if not first:
            continue

        if first.lower() == target_first and last.lower() == target_last:

            hometown = hometown_tag.get_text(strip=True) if hometown_tag else "N/A"
            eligibility = eligibility_tag.get_text(strip=True) if eligibility_tag else "N/A"
            position = position_tag.get_text(strip=True) if position_tag else "N/A"
            height = height_tag.get_text(strip=True) if height_tag else "N/A"

            db.player_identifying_information(
                first, last, hometown, eligibility, position, height
            )

            db.close()

            return {
                "first": first,
                "last": last,
                "school": school,
                "hometown": hometown,
                "eligibility": eligibility,
                "position": position,
                "height": height
            }

    db.close()
    return None
