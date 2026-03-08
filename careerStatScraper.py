import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup


def get_valid_url():
    current_year = datetime.now().year
    url_current = f"https://gomountaineers.com/sports/womens-volleyball/stats/{current_year}"

    if requests.get(url_current).status_code == 200:
        return url_current

    return f"https://gomountaineers.com/sports/womens-volleyball/stats/{current_year - 1}"


def load_tables():

    stats_url = get_valid_url()

    html = requests.get(stats_url).text
    soup = BeautifulSoup(html, "html.parser")

    clean_names = []

    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)

        if "," in text:
            clean_names.append(text)

    tables = pd.read_html(stats_url)

    off_df = tables[3]
    def_df = tables[4]

    def flatten(df):

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.map(
                lambda col: "_".join([str(c).strip() for c in col if str(c) != "nan"])
            )
        else:
            df.columns = df.columns.map(str)

        return df

    off_df = flatten(off_df)
    def_df = flatten(def_df)

    def inject_names(df):

        df = df.copy()

        df["clean_name"] = clean_names[:len(df)]

        df["last"] = df["clean_name"].apply(
            lambda x: x.split(",")[0].strip().lower()
        )

        df["first"] = df["clean_name"].apply(
            lambda x: x.split(",")[1].strip().lower()
        )

        cols_to_drop = [
            c for c in df.columns
            if "player" in c.lower() or "bio" in c.lower()
        ]

        df = df.drop(columns=cols_to_drop, errors="ignore")

        return df

    off_df = inject_names(off_df)
    def_df = inject_names(def_df)

    return off_df, def_df

def scrape_stats(first, last, school):

    off_df, def_df = load_tables()

    first = first.lower()
    last = last.lower()

    offensive_totals = None
    defensive_totals = None

    player_offense = off_df[
        (off_df["first"] == first) & (off_df["last"] == last)
    ]

    player_defense = def_df[
        (def_df["first"] == first) & (def_df["last"] == last)
    ]

    if not player_offense.empty:
        offensive_totals = player_offense.iloc[0].to_dict()

    if not player_defense.empty:
        defensive_totals = player_defense.iloc[0].to_dict()

    return {
        "career": {
            "offensive_stats":{
                

            }
            "defensive_stats": defensive_totals
        }
    }