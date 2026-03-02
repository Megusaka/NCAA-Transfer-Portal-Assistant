import pandas as pd
from datetime import datetime
import requests

#date time documentation 
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.strftime.html
#for current year scalability and to avoid hardcoding 
#https://docs.python-requests.org/en/latest/api
#data cleaning documentation
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.columns.html


def get_valid_url():
    current_year = datetime.now().year 
    url_current = f"https://gomountaineers.com/sports/womens-volleyball/stats/{current_year}"
     # Try current year first 
    if requests.get(url_current).status_code == 200: 
        return url_current 
    
    # Fall back to previous year
    prev_year = current_year - 1 
    url_prev = f"https://gomountaineers.com/sports/womens-volleyball/stats/{prev_year}" 
    return url_prev

tables = pd.read_html(get_valid_url())

print(f"Found {len(tables)} tables\n")

# Loop through the tables and print their content
for i, table in enumerate(tables):
    print(f"--- Table {i} ---")
    print(table)
    print(table.head())
    print("\n")


schedule = tables[7]   # table 7 is the schedule table

# Clean column names (Sidearm sometimes adds spaces)
schedule.columns = schedule.columns.str.strip()

# Print only Date and Opponent columns
#the f-string is used to format the output
#the iterrows() method is used to iterate over the rows of the DataFrame
#the for _ is used to ignore the index value returned by iterrows()
for _, row in schedule.iterrows():
    print(f"{row['Date']} — {row['Opponent']}")
