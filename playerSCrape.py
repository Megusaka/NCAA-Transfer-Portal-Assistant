# my reference for this code is the beautiful soup documentation
# NEED TO RUN IN PYTHON 3.13 Verson
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# https://scrapingant.com/blog/beautifulsoup-cheatsheet
from bs4 import BeautifulSoup
import requests
import DatabaseConnection as DatabaseConnector

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

db = DatabaseConnector.get_db_connection()


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

    name_parts = name.split(" ", 1)
    first_name = name_parts[0]
    last_name = name_parts[1]

    DatabaseConnector.insert_into_player_identifying_information(DatabaseConnector.PlayerIdentifyingInformation(
        pii_id=None, 
        first_name=first_name, 
        last_name=last_name, 
        school=school
        ))

db.close()