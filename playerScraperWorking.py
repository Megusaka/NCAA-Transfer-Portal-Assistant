# # my reference for this code is the beautiful soup documentation
# # NEED TO RUN IN PYTHON 3.13 Verson
# for beatiful soup understanding
# # https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# # https://scrapingant.com/blog/beautifulsoup-cheatsheet
# # https://www.geeksforgeeks.org/python/find-the-siblings-of-tags-using-beautifulsoup/
#app integration 
# # https://medium.com/@partner0307/python-web-scraping-with-flask-a-step-by-step-guide-a0ef33883894

import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup

#need to add a split name function because the user will input first and last name seperately
def full_name(first_name, last_name):
    raw_name = []
    first = first_name
    last = last_name
    player_name = raw_name.append(first,last)
    return player_name
    
#issue here with the getting the access to the array 
#will need to match up the varible name when spinner is added
def school_grab(school):
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
    while match == False:
        school = school
        if school in school_options:
            match == True
        else:
         print("team website not found")

    if match == True:
        return school
    else:
        print("error in accessing the websote")


#adding the url functions to get a working url plug and play
#issue with the array
def get_valid_roster_url():
        current_year = datetime.now().year
        school = school_grab()
        roster_url_working = f"{school}/sports/womens-volleyball/roster/{current_year}"
        if requests.get(roster_url_working).status_code == 200:
            return roster_url_working
        return f"{school}/sports/womens-volleyball/roster/{current_year - 1}"

#i should ba able to pull both career stats and game by game stats from this url nested 
def get_working_carrer_stats_url():
        current_year = datetime.now().year
        school = school_grab() 
        career_stats_working = f"{school}/sports/womens-volleyball/stats/{current_year}"
        if requests.get(career_stats_working).status_code == 200:
            return career_stats_working
        return f"{school}/sports/womens-volleyball/stats/{current_year - 1}"
            

#roster scrape starts here
def scrape_roster(first_name, last_name, school):
    player_summary = []

    first = first_name.strip().lower()
    last = last_name.strip().lower()
    school = school_grab()

    url = get_valid_roster_url(school)

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

        first_name, last_name = full_name(raw_name)

        if first_name and last_name:
            if first_name.lower() == first and last_name.lower() == last:
                return {
                    "first_name": first_name,
                    "last_name": last_name,
                    #"school": school,
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
    summary_complete = player_summary.append(raw_name, hometown_tag, eligibility_tag, position_tag, height_tag) #school?
    
    return summary_complete


def scrape_player_career_stats(first_name, last_name, school):
    player_career_O_stats = []
    player_career_D_stats = []

    first = first_name.strip().lower()
    last = last_name.strip().lower()
    school = school_grab()

    url = get_working_carrer_stats_url(school)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    #getting confused with reading the html for which class name actually needs to be pulled?
    #from documentation : soup.find_all("a", class_="sister")
    #how to identify parent and sibiling tag for beatiful soup raw html?
    offensive = soup.find_all("side-arm-primary", id = "individual-overall-offensive") 
    defensive = soup.find_all("side-arm-primary", id = "induvidual-overall-defensive")

    #look into documentation for the anwser to scraping table and classes specifics
    for o in offensive: 
        SP_tag =o.select_one("text-center")
        MP_tag = o.select_one("text-center")
        MS_tag = o.select_one("text-center")
        pts_tag = o.select_one("text-center")
        pts_s_tag = o.select_one("text-center")
        K_tag = o.select_one("text-center")
        KS_tag = o.select_one("text-center")
        E_tag = o.select_one("text-center")
        TA_tag = o.select_one("text-center")
        PCT_tag = o.select_one("text-center")
        A_tag = o.select_one("text-center")
        AS_tag = o.select_one("text-center")
        SA_tag = o.select_one("text-center")
        SAS_tag = o.select_one("text-center")
        SE_tag = o.select_one("text-center")

        if first_name and last_name:
            if first_name.lower() == first and last_name.lower() == last:
                return {
                    "SP" : SP_tag.get_text(strip=True) if SP_tag else "N/A",
                    "MP" : MP_tag.get_text(strip=True) if MP_tag else "N/A",
                    "MS" : MS_tag.get_text(strip=True) if MS_tag else "N/A",
                    "PTS" : pts_tag.get_text(strip=True) if pts_tag else "N/A",
                    "PTS/S" : pts_s_tag.get_text(strip=True) if pts_s_tag else "N/A",
                    "K" : K_tag.get_text(strip=True) if K_tag else "N/A",
                    "K/S" : KS_tag.get_text(strip=True) if KS_tag else "N/A",
                    "E" : E_tag.get_text(strip=True) if E_tag else "N/A",
                    "PCT" : PCT_tag.get_text(strip=True) if PCT_tag else "N/A",
                    "A" : A_tag.get_text(strip=True) if A_tag else "N/A",
                    "AS" : AS_tag.get_text(strip=True) if AS_tag else "N/A",
                    "SA" : SA_tag.get_text(strip=True) if SA_tag else "N/A",
                    "SAS" : SAS_tag.get_text(strip=True) if SAS_tag else "N/A",
                    "SE" : SE_tag.get_text(strip=True) if SE_tag else "N/A",
                }
            else:
                return("error with player's offensive stats")
        else: 
            return("offensive stats not found")
        
    offensive_scrape = player_career_O_stats.append(SP_tag, MP_tag, MS_tag, pts_tag, pts_s_tag, K_tag, KS_tag, E_tag, PCT_tag, A_tag, AS_tag, SA_tag, SAS_tag, SE_tag)

    for d in defensive:
        SP_tag = d.select_one("text_center")
        Dig_tag = d.select_one("text_center")
        Dig_s_tag = d.select_one("text_center")
        RE_tag = d.select_one("text_center")
        TA_tag = d.select_one("text_center")
        Rec_tag = d.select_one("text_center")
        RE_s_tag = d.select_one("text_center")
        BS_tag = d.select_one("text_center")
        BA_tag = d.select_one("text_center")
        BLK_tag = d.select_one("text_center")
        BLK_S_tag = d.select_one("text_center")
        BE_tag = d.select_one("text_center")
        BHE_tag = d.select_one("text_center")

        if first_name and last_name:
            if first_name.lower() == first and last_name.lower() == last:
                return {
                    "SP" : SP_tag.get_text(strip=True) if SP_tag else "N/A",
                    "DIG" : Dig_tag.get_text(strip=True) if Dig_tag else "N/A",
                    "Dig/S" : Dig_s_tag.get_text(strip=True) if Dig_s_tag else "N/A",
                    "RE" : RE_tag.get_text(strip=True) if RE_tag else "N/A",
                    "TA" : TA_tag.get_text(strip=True) if TA_tag else "N/A",
                    "REC" : Rec_tag.get_text(strip=True) if Rec_tag else "N/A",
                    "RE/S" : RE_s_tag.get_text(strip=True) if RE_s_tag else "N/A",
                    "BS" : BS_tag.get_text(strip=True) if BS_tag else "N/A",
                    "BA" : BA_tag.get_text(strip=True) if BA_tag else "N/A",
                    "BLK" :BLK_tag.get_text(strip=True) if BLK_tag else "N/A",
                    "BLK/S" : BLK_S_tag.get_text(strip=True) if BLK_S_tag else "N/A",
                    "BE" : BE_tag.get_text(strip=True) if BE_tag else "N/A",
                    "BHE" : BHE_tag.get_text(strip=True) if BHE_tag else "N/A",
                }
            else:
                return("error with players defensive stats")
        else:
            return ("defensive stats not found")
        
    defensive_scrape = player_career_D_stats.append(SP_tag, Dig_tag,Dig_s_tag,RE_tag, TA_tag, Rec_tag, RE_s_tag, BS_tag,BA_tag,BLK_tag,BLK_S_tag,BE_tag,BHE_tag)


    return defensive_scrape , offensive_scrape

def scrape_player_match_played(first_name, last_name, school):
     #need to add the scrape that pull from nested nested table that is name specific 
     #will need to add a for lopp to pull all the data that is stored 
    player_games_played = []

    first = first.strip().lower()
    last = last.strip().lower()
    school = school_grab()

    url = get_working_carrer_stats_url(school)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    stats = soup.find_all('sorting')

    for s in stats: 
        date_tag = s.select_all()
        opponet_tag = s.select_all()

        if first_name and last_name:
            if first_name.lower() == first and last_name.lower() == last:
                return {
                    "date": date_tag.get_text(strip=True) if date_tag else "N/A",
                    "opponet": opponet_tag.get_text(strip=True) if opponet_tag else "N/A"
                }
            else:
                return("error with getting the games player participated in")
        else:
            return("player games not found")      
    
    games_played = player_games_played.append(date_tag, opponet_tag)
    
    return games_played
