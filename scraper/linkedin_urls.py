from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from scraper.path import LINKEDIN_COOKIES_FILE

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

def get_linkedin_urls(df, driver):
    """
    Add LinkedIn profile URLs to a list of dictionaries.
    
    :param data: List of dictionaries with 'name' and 'last_name' keys.
    :param driver: Selenium WebDriver instance.
    :return: Updated list of dictionaries with 'linkedin_profile' added.
    """
    for person in df:
        print(person)
        name = person[0]
        last_name = person[1]
        print(f"Searching for {name} {last_name}...")
        
        profile_url = search_person(driver, name, last_name)
        person['linkedin_profile'] = profile_url

    return df
