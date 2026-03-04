from flask import Flask, render_template, request, redirect, url_for
import uuid
import DatabaseConnection as db

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        school = request.form.get("school")

        if first_name and last_name and school:
            pii_id = str(uuid.uuid4())

            db.insert_into_player_identifying_information(
                pii_id,
                first_name,
                last_name,
                school
            )

        return redirect(url_for("index")) #allows for url change


    query = "SELECT pii_id, first_name, last_name, school FROM player_identifying_information ORDER BY first_name"
    players = db.execute_read(query, ())

    return render_template("index.html", players=players)



@app.route("/player/<pii_id>")
def player_detail(pii_id):
    query = """
        SELECT first_name, last_name, school
        FROM player_identifying_information
        WHERE pii_id = %s
    """
    player = db.execute_read(query, (pii_id,))

    return render_template("player_detail.html", player=player)



if __name__ == "__main__":
    app.run(debug=True)
