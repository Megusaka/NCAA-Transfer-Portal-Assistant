import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup


# Automatically determine the correct stats URL.
# Western updates stats pages yearly, so we check the current
# year first and fall back to the previous year if needed.
def get_valid_url():
    current_year = datetime.now().year
    url_current = f"https://gomountaineers.com/sports/womens-volleyball/stats/{current_year}"
    if requests.get(url_current).status_code == 200:
        return url_current
    return f"https://gomountaineers.com/sports/womens-volleyball/stats/{current_year - 1}"

stats_url = get_valid_url()


# Scrape the HTML to extract clean player names.
# The stats tables do NOT include names, so we scrape <a> tags
# that contain "Last, First" format and align them with rows.
html = requests.get(stats_url).text
soup = BeautifulSoup(html, "html.parser")

clean_names = []
for a in soup.find_all("a", href=True):
    text = a.get_text(strip=True)
    if "," in text:  # "Last, First"
        clean_names.append(text)


# Load the stats tables using pandas.
# Table 3 = Offensive stats
# Table 4 = Defensive stats
tables = pd.read_html(stats_url)
off_df = tables[3]
def_df = tables[4]

# Some tables use MultiIndex headers (two-row headers).
# Flatten them into single-level headers for consistency.
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

# Inject the cleaned names into both tables.
# Split "Last, First" into separate lowercase columns.
# Drop irrelevant columns like "Player" or "Bio".
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

def scrape_player(first, last, school):
    # Normalize input for matching
    first = first.strip().lower()
    last = last.strip().lower()

    # Match rows in both tables
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
