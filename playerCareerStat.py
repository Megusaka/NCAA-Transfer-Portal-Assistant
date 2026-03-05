import pandas as pd
from datetime import datetime
import requests

def get_valid_url():
    current_year = datetime.now().year
    url_current = f"https://gomountaineers.com/sports/womens-volleyball/stats/{current_year}"
    if requests.get(url_current).status_code == 200:
        return url_current

    prev_year = current_year - 1
    return f"https://gomountaineers.com/sports/womens-volleyball/stats/{prev_year}"


tables = pd.read_html(get_valid_url())

print(f"Found {len(tables)} tables\n")

# Table 2 = Defensive
table2 = tables[2]

# Table 4 = Offensive
table4 = tables[4]

def flatten(df):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.map(
            lambda col: "_".join([str(c).strip() for c in col if str(c) != "nan"])
        )
    else:
        df.columns = df.columns.map(str)
    return df

table2 = flatten(table2)
table4 = flatten(table4)

print("=== TABLE 2 (DEFENSIVE) COLUMNS ===")
print(table2.columns)

print("\n=== TABLE 2 (DEFENSIVE) ROWS ===")
for _, row in table2.iterrows():
    print(row.to_string())
    print()

print("=== TABLE 4 (OFFENSIVE) COLUMNS ===")
print(table4.columns)

print("\n=== TABLE 4 (OFFENSIVE) ROWS ===")
for _, row in table4.iterrows():
    print(row.to_string())
    print()
