import CareerStatsScraper as css
import PlayerInformationScraper as pis
import GameStatisticsScraper as gss
import DatabaseConnection as db

SCHOOL_URL_MAP = {
    "Adams State" : "https://asugrizzlies.com/sports/womens-volleyball/stats/2025#individual",
    "Black Hills State" : "https://bhsuathletics.com/sports/womens-volleyball/stats#individual",
    "Chadron State" : "https://chadroneagles.com/sports/womens-volleyball/stats/2025#individual",
    "Colorado Christian" : "https://ccucougars.com/sports/womens-volleyball/stats#individual",
    "Colorado Mesa" : "https://cmumavericks.com/sports/womens-volleyball/stats/2025#individual",
    "Colorado School of Mines" : "https://minesathletics.com/sports/womens-volleyball/stats#individual",
    "CSU Pueblo" : "https://gothunderwolves.com/sports/womens-volleyball/stats/2025#individual",
    "Fort Lewis" : "https://goskyhawks.com/sports/womens-volleyball/stats/2025#individual",
    "MSU Denver" : "https://roadrunnersathletics.com/sports/womens-volleyball/stats/2025#individual",
    "New Mexico Highlands" : "https://nmhuathletics.com/sports/womens-volleyball/stats#individual",
    "Regis" : "https://regisrangers.com/sports/womens-volleyball/stats#individual",
    "South Dakota Mines" : "https://gorockers.com/sports/womens-volleyball/stats#individual",
    "UCCS" : "https://gomountainlions.com/sports/womens-volleyball/stats/2025#individual",
    "Western Colorado University" : "https://gomountaineers.com/sports/womens-volleyball/stats/2025#individual",
    "Westminster" : "https://westminstergriffins.com/sports/womens-volleyball/stats/2025?path=wvball#individual"
}

def full_player_scrape_handler(first_name: str, last_name: str, school: str):

    url = SCHOOL_URL_MAP.get(school)
    print(url)

    #Player information first -- we need pii_id for other scrapers
    pis.pii_helper(first_name, last_name, school, url)
    
    css.career_stats_helper(first_name, last_name, school, url)
    gss.game_stats_helper(first_name, last_name, school, url)


# full_player_scrape_handler("Jaylee", "Gonzales", "New Mexico Highlands")
# pii_id = db.get_pii_id_by_name_and_school("Jaylee", "Gonzales", "New Mexico Highlands")
# print(db.get_player_identifying_information_by_pii_id(pii_id))
# print("\n")
# print(db.get_career_statistics_by_pii_id(pii_id))
# print("\n")
# print(db.get_game_statistics_by_pii_id(pii_id))