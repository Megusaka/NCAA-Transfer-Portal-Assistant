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
    "Position": "position",
    "Height": "height",
    "Class": "eligibility",
    "Hometown": "hometown",
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
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--window-size=1920,1080")

    # driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome()
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
        ec.presence_of_all_elements_located((By.CSS_SELECTOR, "div.details"))
    )

    WebDriverWait(driver, 10).until(
        lambda d: any(
            dd.get_attribute("textContent").strip() != "" 
            for dd in d.find_elements(By.CSS_SELECTOR, "div.details dd")
        )
    )

    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    driver.quit()
    return soup

def get_details_string(soup: BeautifulSoup) -> str:
    lines = []
    details = soup.find("div", class_="dialog player-bio player-modal-overlay open")
    if details:
        for dc in details.find_all("div", class_="content"):
            
            #print(dc.prettify())
            di = dc.find_all("div", class_="details")
            for d in di:
                #print(d.prettify())
                dts = d.find_all("dt")
                dds = d.find_all("dd")
                for dt, dd in zip(dts, dds):
                    label = dt.get_text(strip=True).rstrip(":")
                    value = dd.get_text(strip=True)
                    value = " ".join(value.split())
                    lines.append(f"  {label}: {value}")
    else:
        lines.append("No details found")

    return "\n".join(lines)

def player_identifying_info_string_to_dataclass(pii_string: str, first_name: str, last_name: str, school: str) -> db.PlayerIdentifyingInformation:

    mapped_values = {}

    for line in pii_string.splitlines():
        line = line.strip()

        if not line or ":" not in line:
            continue

        label, value = line.split(": ", 1)
        #print(f"Label: '{label}', Value: '{value}'")

        if label in LABEL_MAP:
            field_name = LABEL_MAP[label]
            mapped_values[field_name] = value

    mapped_values["pii_id"] = None
    mapped_values["first_name"] = first_name
    mapped_values["last_name"] = last_name
    mapped_values["school"] = school
    mapped_values["is_favorite"] = False
    mapped_values["contact_status"] = 0

    #print(mapped_values)

    return db.PlayerIdentifyingInformation(**mapped_values)

def pii_helper(first_name: str, last_name: str, school: str, url: str):
    
    soup = get_soup_object(url, first_name, last_name)
    information_string = get_details_string(soup)
    pii_object = player_identifying_info_string_to_dataclass(information_string, first_name, last_name, school)

    db.insert_into_player_identifying_information(pii_object)

pii_helper("Olive", "Rolseth", "Western Colorado University", "https://gomountaineers.com/sports/womens-volleyball/stats/2025#individual")
    
print(db.get_all_player_data())
# soup = get_soup_object("https://gomountaineers.com/sports/womens-volleyball/stats/2025#individual", "Nina", "Cowan")
# details_string = get_details_string(soup)
# print(player_identifying_info_string_to_dataclass(details_string, "Nina", "Cowan", "Western Colorado University"))
#player_identifying_info_string_to_dataclass(details_string, "Nina", "Cowan", "Western Colorado University")