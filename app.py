from flask import Flask, render_template, request, redirect, url_for
import DatabaseConnection as db
import playerScraperWorking as player_scraper


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    player_summary = []
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        school = request.form.get("school")

        player_summary = player_scraper.scrape_roster(first_name, last_name, school )
        player_career_stats = player_scraper.scrape_player_career_stats(first_name, last_name, school)
        player_games_played = player_scraper.scrape_player_match_played(first_name, last_name, school )
        #how would i do this for all the scrape so the user only needs to input it once?
        #dont need to return need to connect the database
        #return player_summary, player_career_stats, player_games_played
        if not first_name or not last_name or not school:
            return redirect(url_for("index"))
        #will add to zoe's write to database file if needed, here just for current access, needs check for redundant add with get_player_id_by_info
        first, last = player_summary["name"].split(" ", 1)
        hometown = player_summary["hometown"]
        eligibility = player_summary["eligibility"]
        position = player_summary["position"]
        height = player_summary["height"]

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
    


    player_career_stats = []
    players = db.get_all_player_data()
    
    for player in players:
        pii_id = player["pii_id"]
        career_stats = db.get_career_statistics_by_pii_id(pii_id)
        for stat in career_stats:
            print(stat["sets_played_offensive"], stat["kills"], stat["assists_per_set"], 
                  stat["errs"], stat["total_attempts"], stat["attack_percentage"],
                   stat["assist"], stat["assists_per_set"], stat["serve_aces"],
                   stat["serve_errors"], stat["serve_aces_per_set"], stat["sets_played_defense"],
                   stat["reception_errors"], stat["digs"], stat["digs_per_set"], stat["block_solos"],
                   stat["block_assists"], stat["blk"], stat["blk_per_s"], stat["block_errors"], 
                   stat["ball_handling_errors"], stat["points"])
        
        game_stats = db.get_game_statistics_by_player_id(pii_id)
        for stat in game_stats:
            print(stat["game_date"], stat["opponet"], stat["sets_played"],
                  stat["kills"], stat["errs"], stat["total_attempts"], stat["attack_percentage"],
                  stat["assists"], stat["service_aces"], stat["service_errors"], stat["reception_errors"],
                  stat["digs"], stat["block_solos"], stat["block_assists"], stat["block_errors"],
                  stat["ball_handling_errors"], stat["total_blocks"]
                )

        if career_stats:
            career_dict = career_stats[0]
        else:
            None

        if game_stats:
            game_dict = game_stats[0]
        else:
            None
        
        player_career_stats.append({
             "identifying" : player,
             "career" : career_dict,
             "gameBygame" : game_dict
        })

    return render_template("index.html", player_career_stats = player_career_stats)
            
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
