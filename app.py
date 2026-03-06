from flask import Flask, render_template, request
import playerCareerStatWorking as stat_scraper
import playerSummaryScrapeWorking as roster_scraper

app = Flask(__name__)

search_history = []

@app.route("/")
def index():
    return render_template("index.html", all_data=search_history)

@app.route("/player", methods=["POST"])
def player():
    first = request.form["first"].strip().lower()
    last = request.form["last"].strip().lower()
    school = request.form["school"].strip()

    stats = stat_scraper.scrape_player(first, last, school)
    roster = roster_scraper.get_roster_info(first, last, school)

    if stats is None:
        return render_template("player_detail.html", careerStats=None)

    identifying = {
        "first_name": first.title(),
        "last_name": last.title(),
        "school": school,
        "hometown": roster.get("hometown", "N/A") if roster else "N/A",
        "eligibility": roster.get("eligibility", "N/A") if roster else "N/A",
        "position": roster.get("position", "N/A") if roster else "N/A",
        "height": roster.get("height", "N/A") if roster else "N/A"
    }

    careerStats = {**stats["offensive"], **stats["defensive"]}

    search_history.append({
        "identifying": identifying,
        "careerStats": careerStats
    })

    return render_template("player_detail.html", careerStats=careerStats)

if __name__ == "__main__":
    app.run(debug=True)