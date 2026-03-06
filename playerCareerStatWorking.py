#sources
# multiIndexing https://stackoverflow.com/questions/79899547/flatten-multindex-column-in-a-pipe-in-pandas
#flattening https://stackoverflow.com/questions/14507794/how-to-flatten-a-hierarchical-index-in-columns
import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def get_valid_stats_url():
    current_year = datetime.now().year
    base = "https://gomountaineers.com/sports/womens-volleyball/stats"

    # Try current year 
    for year in [current_year, current_year - 1]:
        url = f"{base}/{year}"
        if requests.get(url).status_code == 200:
            return url

    return f"{base}/{current_year - 1}"

def load_stats_tables(stats_url):
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

    # Inject names
    def inject_names(df):
        df = df.copy()
        df["clean_name"] = clean_names[:len(df)]

        df["last"] = df["clean_name"].apply(lambda x: x.split(",")[0].strip().lower())
        df["first"] = df["clean_name"].apply(lambda x: x.split(",")[1].strip().lower())

        cols_to_drop = [c for c in df.columns if "player" in c.lower() or "bio" in c.lower()]
        df = df.drop(columns=cols_to_drop, errors="ignore")

        return df

    off_df = inject_names(off_df)
    def_df = inject_names(def_df)

    return off_df, def_df

def scrape_player(first, last, school):
    first = first.strip().lower()
    last = last.strip().lower()

    stats_url = get_valid_stats_url()
    off_df, def_df = load_stats_tables(stats_url)

    # Match rows
    off_match = off_df[(off_df["first"] == first) & (off_df["last"] == last)]
    def_match = def_df[(def_df["first"] == first) & (def_df["last"] == last)]

    if off_match.empty and def_match.empty:
        return None

    def clean_row(row):
        return {
            col: row[col]
            for col in row.index
            if col not in ("clean_name", "first", "last")
        }

    offensive_stats = clean_row(off_match.iloc[0]) if not off_match.empty else {}
    defensive_stats = clean_row(def_match.iloc[0]) if not def_match.empty else {}

    return {
        "first": first,
        "last": last,
        "school": school,
        "offensive": offensive_stats,
        "defensive": defensive_stats
    }
