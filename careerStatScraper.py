import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def split_name(full_name):
    parts = full_name.strip().split()

    if len(parts) == 0:
        return None, None
    if len(parts) == 1:
        return parts[0], ""

    return parts[0], " ".join(parts[1:])

def stat_working_url():
    url = "https://gomountaineers.com/sports/womens-volleyball/roster"
    current_year = datetime.now().year
    if status := requests.get(url).status_code == 200:
        url = f"https://gomountaineers.com/sports/womens-volleyball/roster/{current_year}"
        return url
    else:
        url = f"https://gomountaineers.com/sports/womens-volleyball/roster/{current_year - 1}"
        return url
    
    
def load_stats_tables(stats_url):
    """Return offensive and defensive DataFrames with proper column flattening and name parsing."""
    html = requests.get(stats_url).text
    soup = BeautifulSoup(html, "html.parser")

    # Extract clean player names
    clean_names = []
    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        if "," in text:
            clean_names.append(text)

    tables = pd.read_html(stats_url)
    off_df = tables[3]
    def_df = tables[4]

    # Flatten multi-index headers if needed
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

    # Inject names and split first/last
    def inject_names(df):
        df = df.copy()
        df["clean_name"] = clean_names[:len(df)]
        df["last"] = df["clean_name"].apply(lambda x: x.split(",")[0].strip().lower())
        df["first"] = df["clean_name"].apply(lambda x: x.split(",")[1].strip().lower())
        return df

    return inject_names(off_df), inject_names(def_df)


def scrape_stats(first, last, player_id=0, pii_id=0):
    first = first.strip().lower()
    last = last.strip().lower()
    stats_url = get_stats_url()

    off_df, def_df = load_stats_tables(stats_url)
    off_match = off_df[(off_df["first"] == first) & (off_df["last"] == last)]
    def_match = def_df[(def_df["first"] == first) & (def_df["last"] == last)]

    if off_match.empty and def_match.empty:
        return None

    off = off_match.iloc[0] if not off_match.empty else None
    deff = def_match.iloc[0] if not def_match.empty else None

    def get_val(row, key, default=0):
        if row is None or key not in row:
            return default
        val = row[key]
        if pd.isna(val):
            return default
        return val

    return CareerStatistics(
        player_id=player_id,
        sets_played=get_val(off, "S") or get_val(deff, "S"),
        kills=get_val(off, "K"),
        kills_per_set=get_val(off, "K/S"),
        errs=get_val(off, "E"),
        total_attempts=get_val(off, "ATT"),
        attack_percentage=get_val(off, "PCT"),
        assists=get_val(off, "A"),
        assists_per_set=get_val(off, "A/S"),
        serve_aces=get_val(off, "SA"),
        serve_errors=get_val(off, "SE"),
        serve_aces_per_set=get_val(off, "SA/S"),
        reception_errors=get_val(defe, "RE"),
        digs=get_val(defe, "DIG"),
        digs_per_set=get_val(defe, "DIG/S"),
        block_solos=get_val(defe, "BS"),
        block_assists=get_val(defe, "BA"),
        blk=get_val(defe, "BLK"),
        blk_per_s=get_val(defe, "BLK/S"),
        block_errors=get_val(defe, "BE"),
        ball_handling_errors=get_val(defe, "BHE"),
        points=get_val(off, "PTS"),
        pii_id=pii_id
    )