import CareerStatsScraper as css
import PlayerInformationScraper as pis
import GameStatisticsScraper as gss
import DatabaseConnection as db
from datetime import date

def get_year():
    today = date.today()
    return today.year if (today.month, today.day) > (9, 15) else today.year - 1

SCHOOL_URL_MAP_DATED = {
    "Adams State" : f"https://asugrizzlies.com/sports/womens-volleyball/stats/{get_year()}#individual",
    "Chadron State" : f"https://chadroneagles.com/sports/womens-volleyball/stats/{get_year()}#individual",
    "Colorado Mesa" : f"https://cmumavericks.com/sports/womens-volleyball/stats/{get_year()}#individual",
    "CSU Pueblo" : f"https://gothunderwolves.com/sports/womens-volleyball/stats/{get_year()}#individual",
    "Fort Lewis" : f"https://goskyhawks.com/sports/womens-volleyball/stats/{get_year()}#individual",
    "MSU Denver" : f"https://roadrunnersathletics.com/sports/womens-volleyball/stats/{get_year()}#individual",
    "UCCS" : f"https://gomountainlions.com/sports/womens-volleyball/stats/{get_year()}#individual",
    "Western Colorado University" : f"https://gomountaineers.com/sports/womens-volleyball/stats/{get_year()}#individual",
    "Westminster" : f"https://westminstergriffins.com/sports/womens-volleyball/stats/{get_year()}?path=wvball#individual",
    "West Texas A&M" : f"https://gobuffsgo.com/sports/womens-volleyball/stats/{get_year()}#individual",
    "St. Mary's" : f"https://rattlerathletics.com/sports/womens-volleyball/stats/{get_year()}#individual",
    "UT Tyler" : f"https://uttylerpatriots.com/sports/womens-volleyball/stats/{get_year()}#individual",
    "Texas Woman's" : f"https://twuathletics.com/sports/womens-volleyball/stats/{get_year()}#individual",
    "DBU" : f"https://dbupatriots.com/sports/womens-volleyball/stats/{get_year()}#individual",
    "Western New Mexico" : f"https://wnmumustangs.com/sports/womens-volleyball/stats/{get_year()}#individual",
    "Texas A&M International" : f"https://godustdevils.com/sports/womens-volleyball/stats/{get_year()}#individual",
    "Eastern New Mexico" : f"https://goeasternathletics.com/sports/womens-volleyball/stats/{get_year()}#individual",
    "Missouri Western" : f"https://gogriffons.com/sports/womens-volleyball/stats/{get_year()}#individual",
    "Washburn" : f"https://wusports.com/sports/womens-volleyball/stats/{get_year()}#individual",
    "Central Oklahoma" : f"https://bronchosports.com/sports/womens-volleyball/stats/{get_year()}#individual",
    "Emporia State" : f"https://esuhornets.com/sports/womens-volleyball/stats/{get_year()}#individual",
    "Central Missouri" : f"https://ucmathletics.com/sports/womens-volleyball/stats/{get_year()}#individual",
    "Pittsburg State" : f"https://pittstategorillas.com/sports/womens-volleyball/stats/{get_year()}#individual",
    "Fort Hays State" : f"https://fhsuathletics.com/sports/womens-volleyball/stats/{get_year()}#individual",
    "Arkansas-Fort Smith" : f"https://uafortsmithlions.com/sports/womens-volleyball/stats/{get_year()}#individual",
    "Northwest Missouri" : f"https://bearcatsports.com/sports/womens-volleyball/stats/{get_year()}#individual"
}

SCHOOL_URL_MAP_DATELESS = {
    "Black Hills State" : "https://bhsuathletics.com/sports/womens-volleyball/stats#individual",
    "Colorado Christian" : "https://ccucougars.com/sports/womens-volleyball/stats#individual",
    "Colorado School of Mines" : "https://minesathletics.com/sports/womens-volleyball/stats#individual",
    "New Mexico Highlands" : "https://nmhuathletics.com/sports/womens-volleyball/stats#individual",
    "Regis" : "https://regisrangers.com/sports/womens-volleyball/stats#individual",
    "South Dakota Mines" : "https://gorockers.com/sports/womens-volleyball/stats#individual",
    "Angelo State" : "https://angelosports.com/sports/womens-volleyball/stats#individual",
    "Lubbock Christian" : "https://lcuchaps.com/sports/womens-volleyball/stats#individual",
    "Cameron" : "https://cameronaggies.com/sports/womens-volleyball/stats#individual",
    "Oklahoma Christian" : "https://oceagles.com/sports/womens-volleyball/stats#individual",
    "Texas A&M - Kingsville" : "https://javelinaathletics.com/sports/womens-volleyball/stats#individual",
    "Midwestern State" : "https://msumustangs.com/sports/womens-volleyball/stats#individual",
    "UT Permian Basin" : "https://utpbfalcons.com/sports/womens-volleyball/stats#individual",
    "St. Edward's" : "https://gohilltoppers.com/sports/womens-volleyball/stats#individual",
    "UT Dallas" : "https://utdcomets.com/sports/womens-volleyball/stats#individual",
    "Sul Ross State" : "https://srlobos.com/sports/womens-volleyball/stats/#individual",
    "Newman" : "https://newmanjets.com/sports/womens-volleyball/stats#individual",
    "Missouri Southern" : "https://mssulions.com/sports/womens-volleyball/stats#individual"
}

def full_player_scrape_handler(first_name: str, last_name: str, school: str):

    if SCHOOL_URL_MAP_DATED.get(school):
        url = SCHOOL_URL_MAP_DATED[school]
    elif SCHOOL_URL_MAP_DATELESS.get(school):
        url = SCHOOL_URL_MAP_DATELESS[school]
    else:
        url = None
    print(url)

    #Player information first -- we need pii_id for other scrapers
    pis.pii_helper(first_name, last_name, school, url)
    
    css.career_stats_helper(first_name, last_name, school, url)
    gss.game_stats_helper(first_name, last_name, school, url)


#full_player_scrape_handler("Lilinoe", "Nahinu", "Western Colorado University")
# pii_id = db.get_pii_id_by_name_and_school("Jaylee", "Gonzales", "New Mexico Highlands")
# print(db.get_player_identifying_information_by_pii_id(pii_id))
# print("\n")
# print(db.get_career_statistics_by_pii_id(pii_id))
# print("\n")
# print(db.get_game_statistics_by_pii_id(pii_id))