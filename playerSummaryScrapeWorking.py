from bs4 import BeautifulSoup
import requests
from datetime import datetime

def split_name(full_name):
    parts = full_name.strip().split()
    if len(parts) == 0:
        return None, None
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], " ".join(parts[1:])

# Scalable roster URL finder
# Tries current year → previous year → year before that
def get_valid_roster_url():
    base = "https://gomountaineers.com/sports/womens-volleyball/roster"
    current_year = datetime.now().year

    for year in [current_year, current_year - 1, current_year - 2]:
        url = f"{base}/{year}"
        response = requests.get(url)

        if response.status_code == 200:
            return url

    return base

def get_roster_info(first, last, school):
    first = first.strip().lower()
    last = last.strip().lower()

    roster_url = get_valid_roster_url()
    response = requests.get(roster_url)
    soup = BeautifulSoup(response.content, "html.parser")

    players = soup.select(".sidearm-roster-player")

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

        first_name, last_name = split_name(raw_name)

        if not first_name:
            continue

        if first_name.lower() == first and last_name.lower() == last:
            return {
                "hometown": hometown_tag.get_text(strip=True) if hometown_tag else "N/A",
                "eligibility": eligibility_tag.get_text(strip=True) if eligibility_tag else "N/A",
                "position": position_tag.get_text(strip=True) if position_tag else "N/A",
                "height": height_tag.get_text(strip=True) if height_tag else "N/A",
                "school": school
            }

    return None
