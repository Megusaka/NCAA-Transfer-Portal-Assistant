from flask import Flask, render_template, request, redirect, url_for
import DatabaseConnection as db
import playerSCrape as playerScrape

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        school = request.form.get("school")

        if not first_name or not last_name or not school:
                return redirect(url_for("index"))
#will add to zoe's write to database file if needed, here just for current access, needs check for redundant add with get_player_id_by_info
        scraped_data = playerScrape.scrape_player(first_name, last_name, school)
        first, last = scraped_data["name"].split(" ", 1)

        if scraped_data:
                db.insert_into_player_identifying_information(
                    first, last,
                    scraped_data["school"]

                )

        return redirect(url_for("index")) #allows for url change


    all_data = []
    players = db.get_all_player_data()
    
    for player in players:
        pii_id = player["pii_id"]

        career_stats = db.get_career_statistics_by_pii_id(pii_id)
        for stat in career_stats:
            print(stat["sets_played"], stat["kills"], stat["assists_per_set"])
            
        if career_stats:
            career_dict = career_stats[0]
        else:
            career_dict = {}
        
        all_data.append({
             "identifying" : player,
             "career" : career_dict
        })

    return render_template("index.html", all_data = all_data)

@app.route("/favorites")
def favorites():
    # currently all players until favorites implemented in db
    # eventually filter WHERE favorite = TRUE
    all_data = []
    fav_players = db.get_player_by_favorite()
    for player in fav_players:
        pii_id = player["pii_id"]
        career_stats = db.get_career_statistics_by_pii_id(pii_id)
        if career_stats:
            career_dict = career_stats[0]
        else:
            career_dict = {}
        all_data.append({
            "identifying": player,
            "career": career_dict
        })

    return render_template("favorites.html", all_data=all_data)


@app.route("/player/<int:pii_id>")  #detail view page, show graphs and game stats in future
def player_detail(pii_id):

    career_stats = db.get_career_statistics_by_pii_id(pii_id)

    if not career_stats:
         return redirect(url_for("index"))
    return render_template("player_detail.html", career = career_stats)

if __name__ == "__main__":
    app.run(debug=True)
