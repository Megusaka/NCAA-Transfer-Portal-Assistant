import DatabaseConnection as db
import playerScraperWorking as player_scraper

def insert_into_player_identifying_information(pii);
    if player_summary:
            db.insert_into_player_identifying_information(
                first, last,
                player_summary["school"],
                hometown, 
                eligibility, 
                position,
                height
            )
    return redirect(url_for("index")) #allows for url change

def insert_game_statistics(game_stats):