import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup


def get_valid_stats_url():

    current_year = datetime.now().year
    base = "https://gomountaineers.com/sports/womens-volleyball/stats"

    for year in [current_year, current_year - 1]:

        url = f"{base}/{year}"

        try:
            if requests.get(url).status_code == 200:
                return url
        except:
            continue

    return f"{base}/{current_year-1}"


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



def scrape_player(first, last, school):

    first = first.strip().lower()
    last = last.strip().lower()

    stats_url = get_valid_stats_url()

    off_df, def_df = load_stats_tables(stats_url)

    off_match = off_df[
        (off_df["first"] == first) &
        (off_df["last"] == last)
    ]

    def_match = def_df[
        (def_df["first"] == first) &
        (def_df["last"] == last)
    ]

    if off_match.empty and def_match.empty:
        return None


    off = off_match.iloc[0] if not off_match.empty else None
    deff = def_match.iloc[0] if not def_match.empty else None


    def get_val(row, key):

        if row is None:
            return None

        if key in row:
            return row[key]

        return None

    return {

        "sets_played": get_val(off, "S") or get_val(deff, "S"),

        "kills": get_val(off, "K"),
        "kills_per_set": get_val(off, "K/S"),

        "errs": get_val(off, "E"),
        "total_attempts": get_val(off, "TA"),
        "attack_percentage": get_val(off, "Pct"),

        "assists": get_val(off, "A"),
        "assists_per_set": get_val(off, "A/S"),

        "serve_aces": get_val(off, "SA"),
        "serve_errors": get_val(off, "SE"),
        "serve_aces_per_set": get_val(off, "SA/S"),

        "reception_errors": get_val(deff, "RE"),

        "digs": get_val(deff, "DIG"),
        "digs_per_set": get_val(deff, "DIG/S"),

        "block_solos": get_val(deff, "BS"),
        "block_assists": get_val(deff, "BA"),
        "blk": get_val(deff, "TB"),
        "blk_per_s": get_val(deff, "B/S"),

        "block_errors": get_val(deff, "BE"),
        "ball_handling_errors": get_val(deff, "BHE"),

        "points": get_val(off, "PTS")
    }