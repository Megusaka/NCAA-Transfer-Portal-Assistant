from flask import Flask, render_template, request, redirect, url_for
import DatabaseConnection as db
import playerScraperWorking as player_scraper
import playerDatabaseInserts as playerDatabaseInserts
import playerDatabaseDisplay as playerDatabaseDisplay


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        school = request.form.get("school")
#duplicated inputs for function, just call once here, then can split in the other file
        player_full_scrape = player_scraper.player_full_scrape(first_name, last_name, school )
        #how would i do this for all the scrape so the user only needs to input it once?
        #dont need to return need to connect the database
        if not first_name or not last_name or not school:
            return redirect(url_for("index"))
        #will add to zoe's write to database file if needed, here just for current access, needs check for redundant add with get_player_id_by_info
        #inserts need to be in a seperate file
    
    return render_template("index.html", player_full_scrape = player_full_scrape)

#do i really need these other pages for the display because this is currently scrape i can just call from the functions to make it more 
#convenent for when and where to display data 

@app.route("/player_stats",methods=["GET", "POST"])
def player_career_stats():
    player_details = []
    if request.method == "POST":
    
    return render_template("player_detail.html", player_details = player_details, player_games_played = player_games_played)

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
