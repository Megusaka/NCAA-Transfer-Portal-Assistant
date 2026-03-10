import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup


# GET VALID STATS URL
#this will be changing every year
# added scalibilty to automatically check for the current year and fallback to the previous year if needed
def get_valid_url():
    current_year = datetime.now().year
    url_current = f"https://gomountaineers.com/sports/womens-volleyball/stats/{current_year}"

    if requests.get(url_current).status_code == 200:
        return url_current

    return f"https://gomountaineers.com/sports/womens-volleyball/stats/{current_year - 1}"


def load_tables():
    stats_url = get_valid_url()
    # SCRAPE CLEAN NAMES FROM HTML
    # scraping the player names from the stats page to align them with the stats tables.
    # we look for all anchor tags and extract text that contains a comma

    html = requests.get(stats_url).text
    soup = BeautifulSoup(html, "html.parser")

    clean_names = []
    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        if "," in text:
            clean_names.append(text)

    # SCRAPE TABLES WITH PANDAS
    # we use pandas to read the tables from the stats page.
    # We know from inspection that the 3rd and 4th tables contain the offensive and defensive stats in the html.
    tables = pd.read_html(stats_url)
    off_df = tables[3]
    def_df = tables[4]

    #flattening header if it's a MultiIndex
    # (some tables have multi-level headers which can cause issues)
    # this function will flatten them into single-level by joining with underscores
    # explaining we just convert them to strings. This ensures we have clean column names to work with later
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

    # this function takes a dataframe and adds the cleaned names as a new column.
    # It then splits the cleaned names into 'first' and 'last' columns for easier searching later on.
    #lamba functions to split the clean_name into first and last names
    #also strip any extra whitespace and convert to lowercase for consistent searching
    def inject_names(df):
        df = df.copy()
        df["clean_name"] = clean_names[:len(df)]
        df["last"] = df["clean_name"].apply(lambda x: x.split(",")[0].strip().lower())
        df["first"] = df["clean_name"].apply(lambda x: x.split(",")[1].strip().lower())
        
        #dropping some of the coloums that aren't useful for out purpose 
        cols_to_drop = [c for c in df.columns if "player" in c.lower() or "bio" in c.lower()]
        df = df.drop(columns=cols_to_drop, errors="ignore")
        return df
    
    # we inject the cleaned names into both dataframes so we can easily search for players by name later on
    off_df = inject_names(off_df)
    def_df = inject_names(def_df)

    return off_df, def_df

# this function prints the player's stats if found in the given dataframe.
# It checks for a match based on the first and last name, and if found, it
# prints all the stats for that player which will later on be sorted in the database
def scrape_stats(first, last, school):
    off_df, def_df = load_tables()

    first = first.lower()
    last = last.lower()

    # if we found either defensive or offensive stats, we print the school name.
    # If we didn't find any stats, we print a message indicating the player might be a redshirt or missing stats.
    offensive_totals = None
    defensive_totals = None

    player_offense = off_df[(off_df["first"] == first) & (off_df["last"] == last)]
    player_defense = def_df[(def_df["first"] == first) & (def_df["last"] == last)]

    if not player_offense.empty:
        offensive_totals = player_offense.iloc[0].to_dict()

    if not player_defense.empty:
        defensive_totals = player_defense.iloc[0].to_dict()

    return {
        "offensive": offensive_totals or {},
        "defensive": defensive_totals or {}
    }
