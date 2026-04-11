import CareerStatsScraper as css
import PlayerInformationScraper as pis
import GameStatisticsScraper as gss
import DatabaseConnection as db

def full_player_scrape_handler(first_name: str, last_name: str, school: str):

    url = "https://gomountaineers.com/sports/womens-volleyball/stats/2025#individual"

    #Player information first -- we need pii_id for other scrapers
    pis.pii_helper(first_name, last_name, school, url)
    
    css.career_stats_helper(first_name, last_name, school, url)
    gss.game_stats_helper(first_name, last_name, school, url)


full_player_scrape_handler("Liv", "Marshall", "Western Colorado University")
pii_id = db.get_pii_id_by_name_and_school("Liv", "Marshall", "Western Colorado University")
print(db.get_player_identifying_information_by_pii_id(pii_id))
print("\n")
print(db.get_career_statistics_by_pii_id(pii_id))
print("\n")
print(db.get_game_statistics_by_pii_id(pii_id))