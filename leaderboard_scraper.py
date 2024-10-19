import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

def fetch_leaderboard(url, leaderboard_type):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    if leaderboard_type.lower() == '2v2':
        # Click the first button with class name "slider" to load 2v2 leaderboard
        try:
            button = driver.find_element(By.CLASS_NAME, "slider")
            button.click()

        except Exception as e:
            print(f"Error clicking the button: {e}")

    page_source = driver.page_source
    driver.quit()

    return BeautifulSoup(page_source, 'html.parser')

def scrape_user_data(soup, username):
    user_row = soup.find('div', id=lambda value: value and value.lower() == username.lower())
    if user_row:
        rank = user_row.find('span', class_='rank').text.strip()
        top_gods = [img['alt'] for img in user_row.find_all('img', class_='god-avatar')]

        return {'Rank': rank, 'Username': username, 'Top Gods': top_gods}
    else:
        return None

def main():
    leaderboard_type = input("Choose leaderboard (1v1 or 2v2, press Enter for default 1v1): ").strip().lower() or '1v1'

    if leaderboard_type not in ['1v1', '2v2']:
        print("Invalid leaderboard type. Defaulting to 1v1.")
        leaderboard_type = '1v1'

    leaderboard_url = "https://www.divineknockout.com/leaderboard/"
    soup = fetch_leaderboard(leaderboard_url, leaderboard_type)

    if soup:
        today_date = datetime.now().strftime("%Y-%m-%d")
        file_name = f"user_data_{today_date}_{leaderboard_type}.txt"

        while True:
            input_username = input("Enter a username (or type 'exit' to stop, 'switch' to change leaderboard type): ").strip().lower()

            if input_username == 'exit':
                break
            elif input_username == 'switch':
                new_leaderboard_type = input("Enter new leaderboard type (1v1 or 2v2): ").strip().lower()
                if new_leaderboard_type in ['1v1', '2v2']:
                    leaderboard_type = new_leaderboard_type
                    soup = fetch_leaderboard(leaderboard_url, leaderboard_type)
                    today_date = datetime.now().strftime("%Y-%m-%d")
                    file_name = f"user_data_{today_date}_{leaderboard_type}.txt"
                    print(f"Switched to {leaderboard_type} leaderboard.")
                else:
                    print("Invalid leaderboard type. Switching aborted.")
            else:
                user_data = scrape_user_data(soup, input_username)

                if user_data:
                    print(f"Scraped data for user '{input_username}' on the {leaderboard_type} leaderboard:")
                    print(f"Rank: {user_data['Rank']}")
                    print(f"Top Gods: {', '.join(user_data['Top Gods'])}")

                    # Append data to the file with correct leaderboard type
                    with open(file_name, 'a') as file:
                        file.write(f"\nDate: {today_date}, Rank: {user_data['Rank']}, Username: {user_data['Username']}, Top Gods: {', '.join(user_data['Top Gods'])}")

                    print(f"User data appended to '{file_name}'")
                else:
                    print(f"User '{input_username}' not found on the {leaderboard_type} leaderboard.")
    else:
        print("Exiting due to an error.")

if __name__ == "__main__":
    main()
