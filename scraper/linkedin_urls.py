from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv

def search_person(driver, name, last_name):
    """
    Search for a person on LinkedIn and return their profile URL.
    
    :param driver: Selenium WebDriver instance.
    :param name: First name of the person.
    :param last_name: Last name of the person.
    :return: The LinkedIn profile URL of the person or None if not found.
    """
    search_url = 'https://www.linkedin.com/company/proximusgroup/people/'
    driver.get(search_url)
    time.sleep(4) 

    # Locate the search input field
    search_field = driver.find_element(By.XPATH, "//input[@id='people-search-keywords']")
    search_field.clear()
    search_field.send_keys(f"{name} {last_name}")
    search_field.send_keys(Keys.RETURN)
    time.sleep(4)  

    # Search for the specific person
    profiles = driver.find_elements(By.CSS_SELECTOR, ".org-people-profile-card__profile-info")
    
    for profile in profiles:
        name_element = profile.find_element(By.CSS_SELECTOR, ".artdeco-entity-lockup__title div")
        name_text = name_element.text.strip()

        if name_text.lower() == f"{name.lower()} {last_name.lower()}":
            profile_link = profile.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            return profile_link
    return None

def get_linkedin_urls(input_file, driver):
    """
    Process the input CSV file row by row and return updated rows with LinkedIn profile URLs.
    
    :param input_file: Path to the input CSV file.
    :param driver: Selenium WebDriver instance.
    :return: List of dictionaries with updated LinkedIn profile URLs.
    """
    updated_data = []  

    with open(input_file, mode="r") as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            name = row.get('name')
            last_name = row.get('last_name')

            print(f"Processing: {name} {last_name}...")

            profile_url = search_person(driver, name, last_name)
            row['linkedin_profile'] = profile_url

            updated_data.append(row)  

    return updated_data
