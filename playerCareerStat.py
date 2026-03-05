import pandas as pd
from datetime import datetime
import requests
from app import playerScrape
from bs4 import BeautifulSoup
import DatabaseConnection as DatabaseConnector

def get_valid_url():
    current_year = datetime.now().year
    url_current = f"https://gomountaineers.com/sports/womens-volleyball/stats/{current_year}"
    if requests.get(url_current).status_code == 200:
        return url_current

    prev_year = current_year - 1
    return f"https://gomountaineers.com/sports/womens-volleyball/stats/{prev_year}"


def flatten(df):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.map(
            lambda col: "_".join([str(c).strip() for c in col if str(c) != "nan"])
        )
    else:
        df.columns = df.columns.map(str)
    return df


def split_name(full):
    parts = full.strip().split()
    if len(parts) == 0:
        return None, None
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], " ".join(parts[1:])


def scrape_single_player_stats():
    target_first, target_last, school = scraper_player()

    if target_first is None:
        return []

    tables = pd.read_html(get_valid_url())

    defensive = flatten(tables[4])
    offensive = flatten(tables[3])

    def normalize(df):
        name_col = df.columns[0]
        df["clean_name"] = (
            df[name_col]
            .astype(str)
            .str.replace(r"^\d+\s*", "", regex=True)
            .str.strip()
        )
        df["first"], df["last"] = zip(*df["clean_name"].map(split_name))
        return df

    defensive = normalize(defensive)
    offensive = normalize(offensive)

    def_row = defensive[
        (defensive["first"].str.lower() == target_first) &
        (defensive["last"].str.lower() == target_last)
    ]

    off_row = offensive[
        (offensive["first"].str.lower() == target_first) &
        (offensive["last"].str.lower() == target_last)
    ]

    if def_row.empty and off_row.empty:
        return []

    defensive_stats = def_row.to_dict(orient="records")[0] if not def_row.empty else {}
    offensive_stats = off_row.to_dict(orient="records")[0] if not off_row.empty else {}

    return [
        {
            "first": target_first,
            "last": target_last,
            "school": school,
            "defensive": defensive_stats,
            "offensive": offensive_stats
        }
    ]
