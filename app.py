from flask import Flask, render_template, request, redirect, url_for
import DatabaseConnection as db
import playerScraperWorking as player_scraper


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    summary_complete = []
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        school = request.form.get("school")

        player_summary = player_scraper.scrape_roster(first_name, last_name, school )
        player_career_stats = player_scraper.scrape_player_career_stats(first_name, last_name, school)
        player_games_played = player_scraper.scrape_player_match_played(first_name, last_name, school )
        #how would i do this for all the scrape so the user only needs to input it once?

        return player_summary, player_career_stats, player_games_played
            
    #should i put the append function here?
    #i return summary complete in the scrapeing is thta going to cause issues?
    #what if i have two different arrays doing the exact same thing one was in the scrape one is in the app where does it need to be? 
    return render_template("index.html", summary_complete = summary_complete)

#do i really need these other pages for the display because this is currently scrape i can just call from the functions to make it more 
#convenent for when and where to display data 

@app.route("/player_stats",methods=["GET", "POST"])
def player_career_stats():
    player_details = []
    if request.method == "POST":
        player_stats = player_scraper.scrape_player_career_stats()
        player_games_played = player_scraper.scrape_player_match_played()

        return player_stats, player_games_played
    
    return render_template("player_detail.html", player_details = player_details)

@app.route("/favorites")
def favorites():
    favorite_players = db.get_all_favorite_players()
    return render_template("favorites.html", all_data=favorite_players)



# @app.route("/player/<int:pii_id>")  #detail view page, show graphs and game stats in future
# def player_detail(pii_id):

#     career_stats = db.get_career_statistics_by_pii_id(pii_id)

#     if not career_stats:
#          return redirect(url_for("index"))
#     return render_template("player_detail.html", career = career_stats)


if __name__ == "__main__":
    app.run(debug=True)
