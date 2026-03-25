# # my reference for this code is the beautiful soup documentation
# # NEED TO RUN IN PYTHON 3.13 Verson
# for beatiful soup understanding
# # https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# # https://scrapingant.com/blog/beautifulsoup-cheatsheet
# # https://www.geeksforgeeks.org/python/find-the-siblings-of-tags-using-beautifulsoup/
# # https://www.scraperapi.com/web-scraping/python/
# # https://docs.python.org/3.13/
# # 
#app integration 
# # https://medium.com/@partner0307/python-web-scraping-with-flask-a-step-by-step-guide-a0ef33883894
#scrape from a nested table 
# # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_html.html
# #https://stackoverflow.com/questions/67113087/beautifulsoup-scrape-tags-with-same-class-name
# #look into RE for structure data scrape


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
#looked into both two options a using a dicionary or an array nothing works with either 
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

    #school = ""

    school_options = {
        "black_hills_state": black_hills_state,
        "chadron_state": chadron_state,
        "colorado_christian": colorado_christian,
        "mesa": mesa,
        "mines": mines,
        "pueblo": pueblo,
        "fort_lewis": fort_lewis,
        "msu_denver": msu_denver,
        "regis": regis,
        "south_dakota_mines": south_dakota_mines,
        "uccs": uccs,
        "western": western,
        "westminster": westminster,
        "new_mexico_highlands": new_mexico_highlands,
        "adams": adams,

        # LONE STAR TEAMS
        "angelo_state": angelo_state,
        "lubbock_christian": lubbock_christian,
        "west_texas_aandm": west_texas_aandm,
        "st_marys": st_marys,
        "ut_tyler": ut_tyler,
        "texas_womans": texas_womans,
        "oklahoma_christian": oklahoma_christian,
        "texas_kingsville_aandm": texas_kingsville_aandm,
        "midwestern": midwestern,
        "ut_permian": ut_permian,
        "st_edwards": st_edwards,
        "ut_dallas": ut_dallas,
        "dallas_baptist_dbu": dallas_baptist_dbu,
        "western_new_mexico": western_new_mexico,
        "cameron": cameron,
        "texas_international_aandm": texas_international_aandm,
        "eastern_new_mexico": eastern_new_mexico,
        "sul_ross_state": sul_ross_state
    }

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
        error = f"school is {school}"
        print(error)
        
        if school in school_options:
            match = True
            print("school found")
            break
        else:
            print("team website not found")

    if match == True:
        return school_options[school]
    else:
        print("error in accessing the website")


#adding the url functions to get a working url plug and play
#issue with the array
def get_valid_roster_url(school):
        current_year = datetime.now().year
        school = school_grab()
        roster_url_working = f"{school}/sports/womens-volleyball/roster/{current_year}"
        if requests.get(roster_url_working).status_code == 200:
            return roster_url_working
        return f"{school}/sports/womens-volleyball/roster/{current_year - 1}"

#i should ba able to pull both career stats and game by game stats from this url nested 
def get_working_carrer_stats_url(school):
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
    school = school_grab(school)

    url = get_valid_roster_url(school)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    players = soup.select(".sidearm-roster-player")

    for p in players:
        #select becasue i only want it to return one result 
        name_tag = p.select_one(".sidearm-roster-player-name")
        hometown_tag = p.select_one(".sidearm-roster-player-hometown")
        eligibility_tag = p.select_one(".sidearm-roster-player-academic-year")
        position_tag = p.select_one(".sidearm-roster-player-position-long-short")
        height_tag = p.select_one(".sidearm-roster-player-height")
        
        #the names are stored in one place and there also add the jersey numbers in that column needed data clean up 
        raw_name = name_tag.get_text(strip=True)
        raw_name = raw_name.lstrip("0123456789 ").strip()
        first_name, last_name = full_name(raw_name)

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
    summary_complete = player_summary.append(raw_name,school, hometown_tag, eligibility_tag, position_tag, height_tag) 
    
    return summary_complete


def scrape_player_career_stats(first_name, last_name, school):
    player_career_O_stats = []
    player_career_D_stats = []

    first = first_name.strip().lower()
    last = last_name.strip().lower()
    school = school_grab(school)

    url = get_working_carrer_stats_url(school)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    #getting confused with reading the html for which class name actually needs to be pulled?
    #from documentation : soup.find_all("a", class_="sister") is this better? 
    #how to identify parent and sibiling tag for beatiful soup raw html?
    #what is the clear difference between data-binds and classes? 
    offensive = soup.find_all("side-arm-primary", id = "individual-overall-offensive") 
    defensive = soup.find_all("side-arm-primary", id = "induvidual-overall-defensive")

    #look into documentation for the anwser to scraping table and classes specifics
    for o in offensive: 
        #there is only one result that needs to be returned 
        SP_tag =o.select_one("text-center")
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
        PTS_tag = o.select_one("text-center")

        if first_name and last_name:
            if first_name.lower() == first and last_name.lower() == last:
                return {
                    "sets_played" : SP_tag.get_text(strip=True) if SP_tag else "N/A",
                    "kills" : K_tag.get_text(strip=True) if K_tag else "N/A",
                    "kills_per_set" : KS_tag.get_text(strip=True) if KS_tag else "N/A",
                    "errs" : E_tag.get_text(strip=True) if E_tag else "N/A",
                    "total_attempts" : TA_tag.get_text(strip=True) if TA_tag else "N/A",
                    "attack_percentage" : PCT_tag.get_text(strip=True) if PCT_tag else "N/A",
                    "assists" : A_tag.get_text(strip=True) if A_tag else "N/A",
                    "assists_per_set" : AS_tag.get_text(strip=True) if AS_tag else "N/A",
                    "service_aces" : SA_tag.get_text(strip=True) if SA_tag else "N/A",
                    "service_aces_per_set" : SAS_tag.get_text(strip=True) if SAS_tag else "N/A",
                    "serve_errors" : SE_tag.get_text(strip=True) if SE_tag else "N/A",
                    "points" : PTS_tag.get_text(string=True) if PTS_tag else "N/A",
                }
            else:
                return("error with player's offensive stats")
        else: 
            return("offensive stats not found")
        
    offensive_scrape = player_career_O_stats.append(SP_tag, K_tag, KS_tag, E_tag, PCT_tag, A_tag, AS_tag, SA_tag, SAS_tag, SE_tag, PTS_tag)

    for d in defensive:
        SP_tag = d.select_one("text_center")
        RE_tag = d.select_one("text_center")
        Dig_tag = d.select_one("text_center")
        Dig_s_tag = d.select_one("text_center")
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
                    "sets_played_defense" : SP_tag.get_text(strip=True) if SP_tag else "N/A",
                    "reception_errors" : RE_tag.get_text(strip=True) if RE_tag else "N/A",
                    "digs" : Dig_tag.get_text(strip=True) if Dig_tag else "N/A",
                    "digs_per_set" : Dig_s_tag.get_text(strip=True) if Dig_s_tag else "N/A",
                    "blocks_solos" : BS_tag.get_text(strip=True) if BS_tag else "N/A",
                    "block_assists" : BA_tag.get_text(strip=True) if BA_tag else "N/A",
                    "blk" :BLK_tag.get_text(strip=True) if BLK_tag else "N/A",
                    "blk_per_s" : BLK_S_tag.get_text(strip=True) if BLK_S_tag else "N/A",
                    "block_errors" : BE_tag.get_text(strip=True) if BE_tag else "N/A",
                    "ball_handling_errors" : BHE_tag.get_text(strip=True) if BHE_tag else "N/A",
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
        #it will return multiple result for a specific tag 
        date_tag = s.select_all("text-center")
        opponet_tag = s.select_all("text-center")
        SP_tag = s.select_all("text-center")
        K_tag = s.select_all("text-center")
        E_tag = s.select_all("text-center")
        TA_tag = s.select_all("text-center")
        PCT_tag = s.select_all("text-center")
        AST_tag = s.select_all("text-center")
        SA_tag = s.select_all("text-center")
        SE_tag = s.select_all("text-center")
        RE_tag = s.select_all("text-center")
        DIG_tag = s.select_all("text-center")
        BS_tag = s.select_all("text-center")
        BA_tag = s.select_all("text-center")
        BE_tag = s.select_all("text-center")
        TB_tag = s.select_all("text-center")
        BHE_tag = s.select_all("text-center")

        if first_name and last_name:
            if first_name.lower() == first and last_name.lower() == last:
                return {
                    "game_date": date_tag.get_text(strip=True) if date_tag else "N/A",
                    "opponet": opponet_tag.get_text(strip=True) if opponet_tag else "N/A",
                    "sets_played" : SP_tag.get_text(strip=True) if SP_tag else "N/A",
                    "kills" : K_tag.get_text(strip=True) if K_tag else "N/A",
                    "errs" : E_tag.get_text(strip=True) if E_tag else "N/A",
                    "total_attempts" : TA_tag.get_text(strip=True) if TA_tag else "N/A",
                    "attack_percentage" : PCT_tag.get_text(strip=True) if PCT_tag else "N/A",
                    "assists" : AST_tag.get_text(strip=True) if AST_tag else "N/A",
                    "service_aces" : SA_tag.get_text(strip=True) if SA_tag else "N/A",
                    "service_errors" : SE_tag.get_text(strip=True) if SE_tag else "N/A",
                    "reception_errors" : RE_tag.get_text(strip=True) if RE_tag else "N/A",
                    "dings" : DIG_tag.get_text(strip=True) if DIG_tag else "N/A",
                    "block_solos" : BS_tag.get_text(strip=True) if BS_tag else "N/A",
                    "block_assists" : BA_tag.get_text(strip=True) if BA_tag else "N/A",
                    "block_errors" : BE_tag.get_text(strip=True) if BE_tag else "N/A",
                    "total_blocks" : TB_tag.get_text(strip=True) if TB_tag else "N/A",
                    "ball_handling_errors" : BHE_tag.get_text(strip=True) if BHE_tag else "N/A",
                }
            else:
                return("error with getting the games player participated in")
        else:
            return("player games not found")      
    
    games_played_stats = player_games_played.append(date_tag, opponet_tag, SP_tag, K_tag,E_tag, TA_tag, PCT_tag, AST_tag, SA_tag, SE_tag, RE_tag, DIG_tag, BS_tag, BA_tag, BE_tag, TB_tag, BHE_tag)
    
    return games_played_stats
