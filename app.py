from flask import Flask, render_template, request, redirect, url_for
import DatabaseConnection as db
import FullInformationScraperHandler as ScrapeHandler

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        school = request.form.get("school")

        if not first_name or not last_name or not school:
                return redirect(url_for("index"))
        
        ScrapeHandler.full_player_scrape_handler(first_name, last_name, school)
        
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

    players = db.get_all_player_data()
    player = next((p for p in players if p["pii_id"] == pii_id), None)
    career_stats = db.get_career_statistics_by_pii_id(pii_id)

    if not player:
        return redirect(url_for("index"))

    return render_template("player_detail.html", player=player, career=career_stats)

@app.route("/favorite/<int:pii_id>", methods=["POST"])
def toggle_favorite(pii_id):
    players = db.get_all_player_data()
    player = next((p for p in players if p["pii_id"] == pii_id), None)
    if player:
        new_status = 0 if player["is_favorite"] else 1
        db.update_player_favorite_status(pii_id, new_status)
    return redirect(request.referrer)   #return to same page

@app.route("/status/<int:pii_id>", methods=["POST"])
def update_status(pii_id):
    new_status = request.form.get("contact_status")
    if new_status is not None:
        db.update_player_contact_status(pii_id, int(new_status))
    return redirect(request.referrer)

if __name__ == "__main__":
    app.run(debug=True)