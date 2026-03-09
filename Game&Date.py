import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import DatabaseConnection as DatabaseConnector

#date time documentation 
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.strftime.html
#for current year scalability and to avoid hardcoding 
#https://docs.python-requests.org/en/latest/api
#data cleaning documentation
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.columns.html


def get_valid_url():
    #try the current year first to avoid hardcoding and to ensure scalability for future seasons
    current_year = datetime.now().year 
    url_current = f"https://gomountaineers.com/sports/womens-volleyball/stats/{current_year}"
    if requests.get(url_current).status_code == 200: 
        return url_current 
    
    # Fall back to previous year
    prev_year = current_year - 1 
    url_prev = f"https://gomountaineers.com/sports/womens-volleyball/stats/{prev_year}" 
    return url_prev

tables = pd.read_html(get_valid_url())

response = requests.get(get_valid_url())
#print(response.status_code)


# with beaiutiful soup we can parse the html and extract the player names
#reponse content is the html content of the page that we want to parse and extract 
#the "html.parser" is the parser that we want to use to parse the html content of the page

print(f"Found {len(tables)} tables\n")

# Loop through the tables and print their content
#for i, table in enumerate(tables):
#  print(f"--- Table {i} ---")
#  print(table)
#  print(table.head())
#  print("\n")

schedule = tables[7]   # table 7 is the schedule table

# Clean column names (Sidearm sometimes adds spaces)
schedule.columns = schedule.columns.str.strip()
print(schedule.columns)


db = DatabaseConnector("game_statistics.db")
db.connect()

# Print only Date and Opponent columns
#the f-string is used to format the output
#the iterrows() method is used to iterate over the rows of the DataFrame
#the for _ is used to ignore the index value returned by iterrows()
for _, row in schedule.iterrows():
   print(f"{row['Date']} — {row['Opponent']} — {row['W/L']} - {row['SP']} - {row['K']} - {row['E']} - {row['TA']} - {row['PCT']} - {row['AST']} - {row['SA']} - {row['SE']} - {row['RE']} - {row['DIG']} - {row['BS']} - {row['BA']} - {row['BE']}  - {row['BHE']} - {row['TB']}")


db.insert_schedule(row['Date'], row['Opponent'], row['W/L'], row['SP'], row['K'], row['E'], row['TA'], row['PCT'], row['AST'], row['SA'], row['SE'], row['RE'], row['DIG'], row['BS'], row['BA'], row['BE'],  row['BHE'], row['TB'])
db.close()
#player_career_stat = tables[3] # table  is the player stats table

#player_career_stat.columns = player_career_stat.columns.str.strip()
#print(player_career_stat.columns)
#for _, row in player_career_stat.iterrows():
#    print(f"{row['Player']} — Matches Played: {row['MP']}")