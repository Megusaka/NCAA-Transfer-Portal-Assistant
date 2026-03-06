import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# USER INPUT
#this will be switched to impliment for the database to pull the player
# name and school from the database instead of user input
def get_user_input():
    first = input("Enter FIRST name: ").strip().lower()
    last = input("Enter LAST name: ").strip().lower()
    school = input("Enter SCHOOL name: ").strip()
    if not first:
        return None, None, None
    return first, last, school

# GET VALID STATS URL
#this will be changing every year
# added scalibilty to automatically check for the current year and fallback to the previous year if needed
def get_valid_url():
    current_year = datetime.now().year
    url_current = f"https://gomountaineers.com/sports/womens-volleyball/stats/{current_year}"
    if requests.get(url_current).status_code == 200:
        return url_current
    return f"https://gomountaineers.com/sports/womens-volleyball/stats/{current_year - 1}"

stats_url = get_valid_url()


# SCRAPE CLEAN NAMES FROM HTML
# scraping the player names from the stats page to align them with the stats tables.
# we look for all anchor tags and extract text that contains a comma
html = requests.get(stats_url).text
soup = BeautifulSoup(html, "html.parser")

clean_names = []
for a in soup.find_all("a", href=True):
    text = a.get_text(strip=True)
    if "," in text:  # "Last, First"
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
        df.columns = df.columns.map(lambda col: "_".join([str(c).strip() for c in col if str(c) != "nan"]))
    else:
        df.columns = df.columns.map(str)
    return df

off_df = flatten(off_df)
def_df = flatten(def_df)

# this function takes a dataframe and adds the cleaned names as a new column.
# It then splits the cleaned names into 'first' and 'last' columns for easier searching later on.
def inject_names(df):
    df = df.copy()
    df["clean_name"] = clean_names[:len(df)]

    df["last"] = df["clean_name"].apply(lambda x: x.split(",")[0].strip().lower())
    df["first"] = df["clean_name"].apply(lambda x: x.split(",")[1].strip().lower())
    
    #dropping some of the coloums that aren't useful for out purpose 
    cols_to_drop = [c for c in df.columns if "player" in c.lower() or "bio" in c.lower()]
    df = df.drop(columns=cols_to_drop, errors="ignore")

    return df


off_df = inject_names(off_df)
def_df = inject_names(def_df)

# this function prints the player's stats if found in the given dataframe.
# It checks for a match based on the first and last name, and if found, it
# prints all the stats for that player which will later on be sorted in the database
def print_player_stats(df, title, first, last):
    match = df[(df["first"] == first) & (df["last"] == last)]
    if match.empty:
        return False

    row = match.iloc[0]
    print(f"\n=== {title} ===")
    print(f"Player: {row['first'].title()} {row['last'].title()}")


    for col, val in row.items():
        if col not in ("clean_name", "first", "last"):
            print(f"{col:<20} {val}")
    return True

def main():
    first, last, school = get_user_input()
    if first is None:
        print("No name entered.")
        return

    found_def = print_player_stats(def_df, "DEFENSIVE STATS", first, last)
    found_off = print_player_stats(off_df, "OFFENSIVE STATS", first, last)

    if found_def or found_off:
        print(f"\nSchool: {school}")
    else:
        print(f"\n{first.title()} {last.title()} from {school} either a redshirt or missing stats.")

if __name__ == "__main__":
    main()
