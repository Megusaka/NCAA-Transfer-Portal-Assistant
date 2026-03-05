# my reference for this code is the beautiful soup documentation
# NEED TO RUN IN PYTHON 3.13 Verson
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# https://scrapingant.com/blog/beautifulsoup-cheatsheet
from bs4 import BeautifulSoup
import requests
from database_connector import DatabaseConnector

from bs4 import BeautifulSoup
import requests

western = "https://gomountaineers.com/sports/womens-volleyball/roster"
response = requests.get(western)
soup = BeautifulSoup(response.content, "html.parser")

def split_name(full_name):
    parts = full_name.split()
    if len(parts) == 0:
        return "N/A", "N/A"
    if len(parts) == 1:
        return parts[0], "N/A"
    return parts[0], " ".join(parts[1:])

title_text = soup.title.get_text(strip=True)
school = title_text.split("-")[-1].replace("Athletics", "").strip()

players = soup.select(".sidearm-roster-player")

db = DatabaseConnector("player_identifying_information.db")
db.connect()

for p in players:
    name_tag = p.select_one(".sidearm-roster-player-name")
    hometown_tag = p.select_one(".sidearm-roster-player-hometown")
    eligibility_tag = p.select_one(".sidearm-roster-player-academic-year")
    position_tag = p.select_one(".sidearm-roster-player-position-long-short")
    height_tag = p.select_one(".sidearm-roster-player-height")

    if name_tag:
        name = name_tag.get_text(strip=True)
        name = name.lstrip("0123456789 ").strip()
    else:
        name = "N/A"

    first_name, last_name = split_name(name)

    hometown = hometown_tag.get_text(strip=True) if hometown_tag else "N/A"
    eligibility = eligibility_tag.get_text(strip=True) if eligibility_tag else "N/A"
    position = position_tag.get_text(strip=True) if position_tag else "N/A"
    height = height_tag.get_text(strip=True) if height_tag else "N/A"

    print(f"{first_name} {last_name} | {school} | {hometown} | {eligibility} | {position} | {height}")

    db.player_identifying_information(first_name, last_name, hometown, eligibility, position, height)

db.close()