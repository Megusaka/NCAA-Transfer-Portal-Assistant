import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from DatabaseConnection import DatabaseConnector


def get_valid_url():
    current_year = datetime.now().year
    url_current = f"https://gomountaineers.com/sports/womens-volleyball/stats/{current_year}"
    if requests.get(url_current).status_code == 200:
        return url_current

    prev_year = current_year - 1
    return f"https://gomountaineers.com/sports/womens-volleyball/stats/{prev_year}"


def scrape_schedule():
    tables = pd.read_html(get_valid_url())
    schedule = tables[7]  # Table 7 = schedule

    schedule.columns = schedule.columns.str.strip()
    db = DatabaseConnector("game_statistics.db")
    db.connect()

    schedule_list = []

    for _, row in schedule.iterrows():
        entry = {
            "date": row["Date"],
            "opponent": row["Opponent"],
            "wl": row["W/L"],
            "sp": row["SP"],
            "k": row["K"],
            "e": row["E"],
            "ta": row["TA"],
            "pct": row["PCT"],
            "ast": row["AST"],
            "sa": row["SA"],
            "se": row["SE"],
            "re": row["RE"],
            "dig": row["DIG"],
            "bs": row["BS"],
            "ba": row["BA"],
            "be": row["BE"],
            "bhe": row["BHE"],
            "tb": row["TB"]
        }

        db.insert_schedule(
            entry["date"], entry["opponent"], entry["wl"], entry["sp"],
            entry["k"], entry["e"], entry["ta"], entry["pct"], entry["ast"],
            entry["sa"], entry["se"], entry["re"], entry["dig"], entry["bs"],
            entry["ba"], entry["be"], entry["bhe"], entry["tb"]
        )

        schedule_list.append(entry)

    db.close()

    return schedule_list
