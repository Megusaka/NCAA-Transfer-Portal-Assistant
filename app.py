from flask import Flask, render_template
import pymysql

app = Flask(__name__)

def get_db_connection():
    print("Connecting to SQL")

    connection = pymysql.connect(
        host="localhost",       #"Megusaka.mysql.pythonanywhere-services.com" #http://127.0.0.1:5000/
        user="",
        password="",
        database="",            #Megusaka$database_name
        cursorclass=pymysql.cursors.DictCursor          #returns dictionary instead of just tuple
                                                        #key = column name
    )

    print("Connected")
    return connection


@app.route("/")
def index():
    print("Route /")
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            print("Select Query Executing")

            cursor.execute("SELECT id, name, position FROM players")
            rows = cursor.fetchall()

            print(f"Number of rows returned: {len(rows)}")
            print("Rows:", rows)
        connection.close()
    except Exception as e:
        print("Database error occurred:", e)
        rows = []
    return render_template("index.html", rows=rows)


if __name__ == "__main__":
    print("starting web server")
    app.run(debug=True)