# # my reference for this code is the beautiful soup documentation
# # NEED TO RUN IN PYTHON 3.13 Verson
# # https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# # https://scrapingant.com/blog/beautifulsoup-cheatsheet

import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup

#need to add a split name function because the user will input first and last name seperately


#issue here with the getting the access to the array 
#will need to match up the varible name when spinner is added
def school_grab():
    #RMAC TEAMS
    black_hills_state= "https://bhsuathletics.com" 
    chadron_state = "https://chadroneagles.com"
    colorado_christian = "https://ccucougars.com"
    mesa =  "https://cmumavericks.com"
    mines = "https://minesathletics.com"
    pueblo = "https://gothunderwolves.com"
    fort_lewis = "https://goskyhawks.com"
    msu_denver = "https://roadrunnersathletics.com"
    regis = "https://regisrangers.com"
    south_dakota_mines = "https://gominesathletics.com"
    uccs = "https://gomountainlions.com"
    western = "https://gomountaineers.com"
    westminster = "https://westminstergriffins.com"
    new_mexico_highlands = "https://nmhuathletics.com"
    adams = "https://asugrizzlies.com"

    #LONE STAR TEAMS
    angelo_state = "https://angelosports.com"
    lubbock_christian = "https://lcuchaps.com"
    #the amperzam messed with varible can match it up later? 
    west_texas_aandm = "https://gobuffsgo.com"
    st_marys = "https://rattlerathletics.com/"
    ut_tyler = "https://uttylerpatriots.com"
    texas_womans = "https://twuathletics.com"
    oklahoma_christian = "https://oceagles.com"
    texas_kingsville_aandm = "https://javelinaathletics.com"
    midwestern = "https://msumustangs.com"
    ut_permian = "https://utpbfalcons.com"
    st_edwards = "https://gohilltoppers.com"
    ut_dallas = "https://utdcomets.com"
    dallas_baptist_dbu = "https://dbupatriots.com"
    western_new_mexico = "https://wnmumustangs.com"
    cameron = "https://cameronaggies.com"
    texas_international_aandm = "https://go-dustdevils.com"
    eastern_new_mexico = "https://goeasternathletics.com"
    sul_ross_state = "https://srlobos.com"

    school = ""

    #name it school to match the call from app or maybe switch it so there isn't problems?
    #normalizing the input to match up with the url array 
    school_options = [black_hills_state, chadron_state, colorado_christian, mesa,
            mines, pueblo, fort_lewis, msu_denver, regis, south_dakota_mines,
            uccs, western, westminster, new_mexico_highlands,adams, angelo_state,
            lubbock_christian, west_texas_aandm, st_marys, ut_tyler, texas_womans,
            oklahoma_christian, texas_kingsville_aandm, midwestern, ut_permian, st_edwards,
            ut_dallas,dallas_baptist_dbu, western_new_mexico, cameron, texas_international_aandm,
            eastern_new_mexico, sul_ross_state
        ]
    
    match = False
    if school in school_options:
        match = True
    else: 
        match = False

    if match == True:
         return school
    else:
         return EOFError


#adding the url functions to get a working url plug and play
#issue with the array
def get_valid_roster_url():
        current_year = datetime.datetime.now().year
        school = school_grab()
        roster_url_working = f"{school}/sports/womens-volleyball/roster/{current_year}"
        if requests.get(roster_url_working).status_code == 200:
            return roster_url_working
        return f"{school}/sports/womens-volleyball/roster/{current_year - 1}"

#i should ba able to pull both career stats and game by game stats from this url nested 
def get_working_carrer_stats_url():
        current_year = datetime.datetime.now().year
        school = school_grab() 
        career_stats_working = f"{school}/sports/womens-volleyball/stats/{current_year}"
        if requests.get(career_stats_working).status_code == 200:
            return career_stats_working
        return f"{school}/sports/womens-volleyball/stats/{current_year - 1}"
            

#roster scrape starts here
def scrape_roster(first, last, school):
    player_summary = []

    first = first.strip().lower()
    last = last.strip().lower()

    url = get_valid_roster_url()

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    players = soup.select(".sidearm-roster-player")

    for p in players:

        name_tag = p.select_one(".sidearm-roster-player-name")
        hometown_tag = p.select_one(".sidearm-roster-player-hometown")
        eligibility_tag = p.select_one(".sidearm-roster-player-academic-year")
        position_tag = p.select_one(".sidearm-roster-player-position-long-short")
        height_tag = p.select_one(".sidearm-roster-player-height")

        raw_name = name_tag.get_text(strip=True)
        raw_name = raw_name.lstrip("0123456789 ").strip()

        first_name, last_name = split_name(raw_name)

        if first_name and last_name:
            if first_name.lower() == first and last_name.lower() == last:

                return {
                    "first_name": first_name,
                    "last_name": last_name,
                    "school": school,
                    "hometown": hometown_tag.get_text(strip=True) if hometown_tag else "N/A",
                    "eligibility": eligibility_tag.get_text(strip=True) if eligibility_tag else "N/A",
                    "position": position_tag.get_text(strip=True) if position_tag else "N/A",
                    "height": height_tag.get_text(strip=True) if height_tag else "N/A"
                }
            else:
                return("error with getting player summary.")
        else: 
            return("player not found.")
    #in the documentation
    summary_complete = player_summary.append(raw_name, school, hometown_tag, eligibility_tag, position_tag, height_tag)
    
    return summary_complete


def scrape_player_career_stats(first, last, school):
    player_career_stats = []

    first = first.strip().lower()
    last = last.strip().lower()

    url = get_working_carrer_stats_url()

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    #look into documentation for the anwser to scraping table and classes specifics

def scrape_player_match_played():
     #need to add the scrape that pull from nested nested table that is name specific 
     #will need to add a for lopp to pull all the data that is stored 
     





