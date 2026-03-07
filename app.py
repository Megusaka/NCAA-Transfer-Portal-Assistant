from flask import Flask, render_template, request
import database_connector as db
import playerScraperWorking as player_scraper

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    player_summary = []
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        school = request.form.get("school")

        player_data = player_scraper.scrape_player(first_name, last_name, school)
        if player_data:
            pii = db.PlayerIdentifyingInformation(
                pii_id=None,
                first_name=player_data["identifying"]["first_name"],
                last_name=player_data["identifying"]["last_name"],
                school=player_data["identifying"]["school"],
                hometown=player_data["identifying"]["hometown"],
                eligibility=player_data["identifying"]["eligibility"],
                position=player_data["identifying"]["position"],
                height=player_data["identifying"]["height"]
            )
            db.insert_into_player_identifying_information(pii)

            player_summary.append(player_data)

    return render_template("index.html", player_summary=player_summary)

@app.route("/favorites")
def favorites():
    favorite_players = db.get_all_favorite_players() 
    return render_template("favorites.html", all_data=favorite_players)


if __name__ == "__main__":
    app.run(debug=True)