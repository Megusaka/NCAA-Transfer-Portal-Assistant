from flask import Flask, render_template, request, redirect, url_for
import database_connector as db
import playerSummaryScrapeWorking as playerScrapeSummary
import playerCareerStatWorking as careerScrape

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():

    summary_data = []

    if request.method == "POST":

        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        school = request.form.get("school")

        # scrape roster info
        summary_data = playerScrapeSummary.scrape_player(
            first_name,
            last_name,
            school
        )

        # scrape career stats
        career_stats = careerScrape.scrape_player(
            first_name,
            last_name,
            school
        )

        if summary_data:

            # create PlayerIdentifyingInformation object
            pii = db.PlayerIdentifyingInformation(
                pii_id=None,
                first_name=first_name,
                last_name=last_name,
                school=school
            )

            # check if player exists
            pii_id = db.get_player_id_by_information(pii)

            if not pii_id:
                db.insert_into_player_identifying_information(pii)
                pii_id = db.get_player_id_by_information(pii)

            # insert career stats if they exist
            if career_stats:

                career = db.CareerStatistics(
                    player_id=None,
                    sets_played=career_stats.get("sets_played"),
                    kills=career_stats.get("kills"),
                    kills_per_set=career_stats.get("kills_per_set"),
                    errs=career_stats.get("errs"),
                    total_attempts=career_stats.get("total_attempts"),
                    attack_percentage=career_stats.get("attack_percentage"),
                    assits=career_stats.get("assists"),
                    assists_per_set=career_stats.get("assists_per_set"),
                    serve_aces=career_stats.get("serve_aces"),
                    serve_errors=career_stats.get("serve_errors"),
                    serve_aces_per_set=career_stats.get("serve_aces_per_set"),
                    reception_errors=career_stats.get("reception_errors"),
                    digs=career_stats.get("digs"),
                    digs_per_set=career_stats.get("digs_per_set"),
                    block_solos=career_stats.get("block_solos"),
                    block_assists=career_stats.get("block_assists"),
                    blk=career_stats.get("blk"),
                    blk_per_s=career_stats.get("blk_per_s"),
                    block_errors=career_stats.get("block_errors"),
                    ball_handling_errors=career_stats.get("ball_handling_errors"),
                    points=career_stats.get("points"),
                    pii_id=pii_id
                )

                db.insert_into_career_statistics(career)

    return render_template("index.html", summary_data=summary_data)


@app.route("/favorites")
def favorites():

    all_data = []

    players = db.get_all_player_data()

    for player in players:

        pii_id = player["pii_id"]

        career_stats = db.get_career_statistics_by_pii_id(pii_id)

        career_dict = career_stats[0] if career_stats else {}

        all_data.append({
            "identifying": player,
            "career": career_dict
        })

    return render_template("favorites.html", all_data=all_data)


@app.route("/player/<int:pii_id>")
def player_detail(pii_id):

    career_stats = db.get_career_statistics_by_pii_id(pii_id)

    if not career_stats:
        return redirect(url_for("index"))

    return render_template("player_detail.html", career=career_stats)


if __name__ == "__main__":
    app.run(debug=True)