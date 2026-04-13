from cProfile import label

from bs4 import BeautifulSoup
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import DatabaseConnection as db


LABEL_MAP = {
    ("SP", 0): "sets_played",
    ("PTS", 0): "points",
    ("K", 0): "kills",
    ("K/S", 0): "kills_per_set",
    ("E", 0): "errs",
    ("TA", 0): "total_attempts",
    ("PCT", 0): "attack_percentage",
    ("A", 0): "assists",
    ("A/S", 0): "assists_per_set",
    ("SA", 0): "serve_aces",
    ("SA/S", 0): "serve_aces_per_set",
    ("SE", 0): "serve_errors",
    ("DIG", 0): "digs",
    ("DIG/S", 0): "digs_per_set",
    ("RE", 0): "reception_errors",
    ("BS", 0): "block_solos",
    ("BA", 0): "block_assists",
    ("BLK", 0): "blk",
    ("BLK/S", 0): "blk_per_s",
    ("BE", 0): "block_errors",
    ("BHE", 0): "ball_handling_errors",
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

def get_soup_object(url: str) -> BeautifulSoup:
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    WebDriverWait(driver, 10).until(lambda d:
        d.find_element(By.ID, "DataTables_Table_0"))

    soup = BeautifulSoup(driver.page_source, 'lxml')
    driver.quit()
    return soup

def get_table0_string(soup: BeautifulSoup, first_name: str, last_name: str) -> str:
    lines = []
    table0 = soup.find("table", id="DataTables_Table_0")
    if table0:
        for row in table0.find_all("tr"):
            cells = row.find_all("td")
            if not cells:
                continue

            is_target_player = False
            
            # Check  if the player's name in row
            for cell in cells:
                name_tag = cell.find("a", {"data-player-id": True})
                if name_tag:
                    value = name_tag.get_text(strip=True)
                    player_first_name, player_last_name = split_name(value)
                    if player_first_name == first_name and player_last_name == last_name:
                        is_target_player = True
                        break
                else:
                    cell_text = cell.get_text(strip=True)
                    if first_name in cell_text and last_name in cell_text:
                        is_target_player = True
                        break

            if not is_target_player:
                continue

            lines.append("Next Player")
            for cell in cells:
                label = cell.get("data-label")
                name_tag = cell.find("a", {"data-player-id": True})
                
                if name_tag:
                    label = "Player"
                    value = name_tag.get_text(strip=True)
                else:
                    value = cell.text.strip()
                    value = " ".join(value.split())
                    
                lines.append(f"  {label}: {value}")
    else:
        lines.append("No table found")
        
    return "\n".join(lines)


def get_table1_string(soup: BeautifulSoup, first_name: str, last_name: str) -> str:
    lines = []
    table1 = soup.find("table", id="DataTables_Table_1")
    if table1:
        for row in table1.find_all("tr"):
            cells = row.find_all("td")
            if not cells:
                continue

            is_target_player = False
            
            # Check  if the player's name in row
            for cell in cells:
                name_tag = cell.find("a", {"data-player-id": True})
                if name_tag:
                    value = name_tag.get_text(strip=True)
                    player_first_name, player_last_name = split_name(value)
                    if player_first_name == first_name and player_last_name == last_name:
                        is_target_player = True
                        break
                else:
                    cell_text = cell.get_text(strip=True)
                    if first_name in cell_text and last_name in cell_text:
                        is_target_player = True
                        break

            if not is_target_player:
                continue

            lines.append("Next Player")
            for cell in cells:
                label = cell.get("data-label")
                name_tag = cell.find("a", {"data-player-id": True})
                
                if name_tag:
                    label = "Player"
                    value = name_tag.get_text(strip=True)
                else:
                    value = cell.text.strip()
                    value = " ".join(value.split())
                    
                lines.append(f"  {label}: {value}")
    else:
        lines.append("No table found")
        
    return "\n".join(lines)

# def get_table1_string(soup: BeautifulSoup) -> str:
#     lines = []
#     table1 = soup.find("table", id="DataTables_Table_1")
#     if table1:
#         for row in table1.find_all("tr"):
#             cells = row.find_all("td")
#             if not cells:
#                 continue

#             lines.append("Next Player")
#             for cell in cells:
#                 label = cell.get("data-label")
#                 name_tag = cell.find("a", {"data-player-id": True})
#                 if name_tag:
#                     label = "Player"
#                     value = name_tag.get_text(strip=True)
#                 else:
#                     value = cell.text.strip()
#                 lines.append(f"  {label}: {value}")
#     else:
#         lines.append("No table found")
#     return "\n".join(lines)

def player_career_stats_string_to_dataclass(career_stats_string: str, school: str) -> db.CareerStatistics:

    mapped_values = {}
    label_counts = defaultdict(int)
    first_name = ""
    last_name = ""

    for line in career_stats_string.splitlines():
        line = line.strip()
        
        if not line or ": " not in line:
            continue

        label, value = line.split(": ", 1)
        label = label.strip()
        value = value.strip()

        current_count = label_counts[label]

        if label == "Player" and current_count == 0:
            if ", " in value:
                last_name, first_name = value.split(", ", 1)
            else:
                last_name = value

        map_key = (label, current_count)
        if map_key in LABEL_MAP:
            field_name = LABEL_MAP[map_key]
            mapped_values[field_name] = auto_cast(value)
        
        label_counts[label] += 1

    pii_id = db.get_pii_id_by_name_and_school(first_name, last_name, school)
    mapped_values["pii_id"] = pii_id
    
    mapped_values["player_id"] = None

    return db.CareerStatistics(**mapped_values)


def career_stats_helper(first_name: str, last_name: str, school: str, url: str):
    
    offensive_url = url + "-overall-offensive"
    defensive_url = url + "-overall-defensive"

    offensive_soup_object = get_soup_object(offensive_url)
    defensive_soup_object = get_soup_object(defensive_url)

    offensive_string = get_table0_string(offensive_soup_object, first_name, last_name)
    defensive_string = get_table1_string(defensive_soup_object, first_name, last_name)

    full_career_string = offensive_string + "\n" + defensive_string

    career_stats = player_career_stats_string_to_dataclass(full_career_string, school)

    db.insert_into_career_statistics(career_stats)

#career_stats_helper("Nina", "Cowan", "Western Colorado University")

# offensive = get_soup_object("https://gomountaineers.com/sports/womens-volleyball/stats/2025#individual-overall-offensive")
# defensive = get_soup_object("https://gomountaineers.com/sports/womens-volleyball/stats/2025#individual-overall-defensive")

# full_career_string = get_table0_string(offensive, "Olive", "Rolseth") + "\n" + get_table1_string(defensive, "Olive", "Rolseth")

# print(player_career_stats_string_to_dataclass(full_career_string, "Western Colorado University"))

# print(get_table0_string(offensive, "Olive", "Rolseth"))
# print(get_table1_string(defensive, "Olive", "Rolseth"))

#print(get_career_stats("Olivia", "Rolseth", "Western Colorado University"))

#print(soupPretty)
#print(soupText)

#print(split_name("Kaalele, Anuhea"))
