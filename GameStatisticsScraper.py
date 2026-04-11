from bs4 import BeautifulSoup
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ec
import time
import DatabaseConnection as db

LABEL_MAP = {
    "Date": "game_date",
    "Opponent": "opponent",
    "SP": "sets_played",
    "K": "kills",
    "E": "errs",
    "TA": "total_attempts",
    "PCT": "attack_percentage",
    "AST": "assists",
    "SA": "serve_aces",
    "SE": "serve_errors",
    "RE": "reception_errors",
    "DIG": "digs",
    "BS": "block_solos",
    "BA": "block_assists",
    "BE": "block_errors",
    "TB": "total_blocks",
    "BHE": "ball_handling_errors",
}

def split_name(full_name: str) -> (str, str):
    parts = full_name.split(", ")
    if len(parts) == 2:
        return parts[1], parts[0]
    return full_name, ""

# Helper to automatically cast strings to int or float
def auto_cast(value: str):
    if not value or value == "-": 
        return None
        
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value
        
def get_soup_object(url: str, first_name: str, last_name: str) -> BeautifulSoup:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.ID, "DataTables_Table_0"))
    )

    # Find the link by matching the player's name in the anchor text
    player_name = f"{last_name}, {first_name}"  # matches format "Rolseth, Olive"
    player_link = driver.find_element(By.LINK_TEXT, player_name)
    player_link.click()

    # Wait for the details subtable to appear
    WebDriverWait(driver, 30).until(
        ec.presence_of_all_elements_located((By.CSS_SELECTOR, "div.stats"))
    )

    WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH, "//caption[contains(text(), 'Game By Game Statistics')]"))
    )

    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    driver.quit()
    return soup

def get_game_table_as_string(soup: BeautifulSoup) -> str:
    lines = []
    
    if not soup:
        return "No table found"
    
    target_table = None
    for table in soup.find_all("table"):
        caption = table.find("caption")
        if caption and "Game By Game Statistics" in caption.get_text():
            target_table = table
            break
            
    if not target_table:
        return "Game By Game table not found"

    # 1. Extract headers dynamically
    thead = target_table.find("thead")
    if not thead:
        return "No header found in table"
        
    header_rows = thead.find_all("tr")
    labels = []
    
    # The table has two header rows. Some headers span 2 rows (rowspan="2"), 
    # while others are grouped under categories (colspan).
    if len(header_rows) >= 2:
        top_headers = header_rows[0].find_all("th")
        bottom_headers = header_rows[1].find_all("th")
        
        # We know Date, Opponent, and SP are the first three (rowspan=2)
        labels.append(top_headers[0].get_text(strip=True)) # Date
        labels.append(top_headers[1].get_text(strip=True)) # Opponent
        labels.append(top_headers[2].get_text(strip=True)) # SP
        
        # The next headers come from the second row (K, E, TA, PCT, AST, etc.)
        for th in bottom_headers:
            labels.append(th.get_text(strip=True))
            
        # The last header (BHE) is at the end of the top row (rowspan=2)
        labels.append(top_headers[-1].get_text(strip=True))
    else:
        # Fallback if there's only one header row for some reason
        print("We fell back")
        labels = [th.get_text(strip=True) for th in header_rows[0].find_all("th")]

    print(labels)

    # 2. Extract and format the data rows
    tbody = target_table.find("tbody")
    if not tbody:
        return "No data body found"

    rows = tbody.find_all("tr")
    
    for row in rows:
        # We need to find both 'td' and 'th' because 'Opponent' is in a <th> tag
        cells = row.find_all(["td", "th"])
        
        if not cells or len(cells) != len(labels):
            continue

        lines.append("Next Game")
        for label, cell in zip(labels, cells):
            # If there's an anchor tag (like in Opponent), get text from it cleanly
            value = cell.get_text(separator=" ", strip=True)
            lines.append(f"  {label}: {value}")

    return "\n".join(lines)

def player_game_stats_string_to_dataclass_array(game_stats_string: str, pii_id: int) -> list[db.GameStatistics]:

    games = []
    current_game = {}

    for line in game_stats_string.splitlines():
        line = line.strip()

        if line == "Next Game":
            if current_game:
                games.append(db.GameStatistics(**current_game))
            current_game = {"pii_id": pii_id}
            continue

        if not line or ": " not in line:
            continue

        label, value = line.split(": ", 1)
        label = label.strip()
        value = value.strip()

        if label in LABEL_MAP:
            field_name = LABEL_MAP[label]
            current_game[field_name] = auto_cast(value)
        
        current_game["game_id"] = None

    if current_game:
        games.append(db.GameStatistics(**current_game))

    return games


def game_stats_helper(first_name: str, last_name: str, school: str, url: str):
    soup = get_soup_object(url, first_name, last_name)
    game_table_string = get_game_table_as_string(soup)
    pii_id = db.get_pii_id_by_name_and_school(first_name, last_name, school)
    game_stats_array = player_game_stats_string_to_dataclass_array(game_table_string, pii_id)

    for game_stat in game_stats_array:
        db.insert_game_statistics(game_stat)

# def get_table_19_as_string(soup: BeautifulSoup) -> str:
#     lines = []
#     #print(soup.prettify())
#     table = soup.find("table", class_="sidearm-table sortable-table dataTable no-footer")
#     print(table.prettify())

# soup = get_soup_object("https://gomountaineers.com/sports/womens-volleyball/stats/2025#individual", "Olive", "Rolseth")
# game_table_string = get_game_table_as_string(soup)
# game_stats_array = player_game_stats_string_to_dataclass_array(game_table_string, 1)

# for game in game_stats_array:
#     print(game)

#game_stats_helper("Olive", "Rolseth", "Western Colorado University", "https://gomountaineers.com/sports/womens-volleyball/stats/2025#individual")

print(db.get_game_statistics_by_pii_id(4))



