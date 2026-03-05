# my reference for this code is the beautiful soup documentation
# NEED TO RUN IN PYTHON 3.13 Verson
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# https://scrapingant.com/blog/beautifulsoup-cheatsheet
from bs4 import BeautifulSoup
import requests
from database_connector import DatabaseConnector

#hard coding the url of the roster page 
#getting the roster page and requsting the content of the page 
#the requests library is used to send an HTTP request to the specified URL and get the response from the server.
#get() method is used to send a GET request to the specifc stored varibles 

western = "https://gomountaineers.com/sports/womens-volleyball/roster"
#mines = 
#mesa = 

url= western

response = requests.get(url)
#print(response.status_code)

# with beaiutiful soup we can parse the html and extract the player names
#reponse content is the html content of the page that we want to parse and extract 
#the "html.parser" is the parser that we want to use to parse the html content of the page
soup = BeautifulSoup(response.content, "html.parser")

def split_name(full_name):
    parts = full_name.split()
    if len(parts) == 0:
        return "N/A", "N/A"
    if len(parts) == 1:
        return parts[0], "N/A"
    return parts[0], " ".join(parts[1:])

# taking the list of players from the html by looking at the html structure 
# the players are in a list item with the class "sidearm-roster-player"
# use the select method to get all the list items with that class
#li is a list item in html and the class is "sidearm-roster-player" which contains the player names
#span is also a class with player info 
players = soup.select(".sidearm-roster-player")
hometown = soup.select(".sidearm-roster-player-hometown")
eligibility = soup.select(".sidearm-roster-player-academic-year")
position = soup.select(".sidearm-roster-player-position-long-short")
height = soup.select(".sidearm-roster-player-height")

# we can then loop through the list of players and other attributes of each player
# the name of each player is in a div with the class "sidearm-roster-player-name"
# we can use the select_one method to get the first div with that class 
# the get_text method to get the text of that div which is the name of the player
#allowing the name to be printed stripping any extra whitespace

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
        name = "N\\A"

    first_name, last_name = split_name(name)

    hometown = hometown_tag.get_text(strip=True) if hometown_tag else "N\\A"
    eligibility = eligibility_tag.get_text(strip=True) if eligibility_tag else "N\\A"   
    position = position_tag.get_text(strip=True) if position_tag else "N\\A"
    height = height_tag.get_text(strip=True) if height_tag else "N\\A"
    print(name + " | " + hometown + " | " + eligibility + " | " + position + " | " + height)

    db.player_identifying_information(first_name, last_name, hometown, eligibility, position, height)

db.close()