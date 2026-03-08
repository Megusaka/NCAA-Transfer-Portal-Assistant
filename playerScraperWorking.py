import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# ROSTER SCRAPER starts here
def split_name(full_name):
    parts = full_name.strip().split()

    if len(parts) == 0:
        return None, None
    if len(parts) == 1:
        return parts[0], ""

    return parts[0], " ".join(parts[1:])


def get_roster_url():
    return "https://gomountaineers.com/sports/womens-volleyball/roster"


def scrape_roster(first, last, school):

    first = first.strip().lower()
    last = last.strip().lower()

    url = get_roster_url()

    response = requests.get(url)
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

        if first_name and last_name:
            if first_name.lower() == first and last_name.lower() == last:

                return {
                    "name": raw_name,
                    "school": school,
                    "hometown": hometown_tag.get_text(strip=True) if hometown_tag else "N/A",
                    "eligibility": eligibility_tag.get_text(strip=True) if eligibility_tag else "N/A",
                    "position": position_tag.get_text(strip=True) if position_tag else "N/A",
                    "height": height_tag.get_text(strip=True) if height_tag else "N/A"
                }

    return None


def scrape_player(first, last, school):

    roster = scrape_roster(first, last, school)

    if roster is None:
        return None

    if "name" in roster:
        parts = roster["name"].split()
        first_name = parts[0]
        last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
    else:
        first_name = ""
        last_name = ""

    return {
        "identifying": {
            "first_name": first_name,
            "last_name": last_name,
            "school": roster.get("school", ""),
            "hometown": roster.get("hometown", ""),
            "eligibility": roster.get("eligibility", ""),
            "position": roster.get("position", ""),
            "height": roster.get("height", "")
        }
    }
