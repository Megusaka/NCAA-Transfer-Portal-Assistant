from bs4 import BeautifulSoup
import requests

def get_user_input():
    user_input = input("Enter player name (first and last): ").strip()
    parts = user_input.split()

    if len(parts) == 0:
        print("No name entered.")
        return None, None, None

    if len(parts) == 1:
        first = parts[0].lower()
        last = ""
    else:
        first = parts[0].lower()
        last = " ".join(parts[1:]).lower()

    school = input("Enter school name: ").strip()
    return first, last, school


def split_name(full_name):
    parts = full_name.strip().split()
    if len(parts) == 0:
        return None, None
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], " ".join(parts[1:])


def scrape_player():
    target_first, target_last, user_school = get_user_input()

    if target_first is None:
        print("No name entered.")
        return None

    url = "https://gomountaineers.com/sports/womens-volleyball/roster"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    players = soup.select(".sidearm-roster-player")

    found = False

    for p in players:
        name_tag = p.select_one(".sidearm-roster-player-name")
        hometown_tag = p.select_one(".sidearm-roster-player-hometown")
        eligibility_tag = p.select_one(".sidearm-roster-player-academic-year")
        position_tag = p.select_one(".sidearm-roster-player-position-long-short")
        height_tag = p.select_one(".sidearm-roster-player-height")

        if not name_tag:
            continue

        raw_name = name_tag.get_text(strip=True)
        raw_name = raw_name.lstrip("0123456789 ").strip()

        first_name, last_name = split_name(raw_name)

        if not first_name:
            continue

        if first_name.lower() == target_first and last_name.lower() == target_last:
            found = True

            hometown = hometown_tag.get_text(strip=True) if hometown_tag else "N/A"
            eligibility = eligibility_tag.get_text(strip=True) if eligibility_tag else "N/A"
            position = position_tag.get_text(strip=True) if position_tag else "N/A"
            height = height_tag.get_text(strip=True) if height_tag else "N/A"

            print("\nMATCH FOUND:")
            print(f"Name: {first_name} {last_name}")
            print(f"School: {user_school}")
            print(f"Hometown: {hometown}")
            print(f"Eligibility: {eligibility}")
            print(f"Position: {position}")
            print(f"Height: {height}\n")

            return

    if not found:
        print("Player not found on roster.")

if __name__ == "__main__":
    scrape_player()
