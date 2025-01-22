from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from path import LINKEDIN_COOKIES_FILE

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
    try:
        profiles = driver.find_elements(By.CSS_SELECTOR, ".org-people-profile-card__profile-info")
        
        for profile in profiles:
            name_element = profile.find_element(By.CSS_SELECTOR, ".artdeco-entity-lockup__title div")
            name_text = name_element.text.strip()

            if name_text.lower() == f"{name.lower()} {last_name.lower()}":
                profile_link = profile.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                return profile_link
        
        return None
    
    except Exception as e:
        print(f"Error while searching for {name} {last_name}: {e}")
        return None

def get_linkedin_url(df, driver):
    """Add LinkedIn profile URLs to the DataFrame.
    
    :param df: Dataframe.
    :param driver: Selenium WebDriver instance.
    """
    profile_urls = []

    for index, row in df.iterrows():
        name = row['name']
        last_name = row['last_name']
        print(f"Searching for {name} {last_name}...")

        profile_url = search_person(driver, name, last_name)
        profile_urls.append(profile_url)

    df['linkedin_profile'] = profile_urls
    
    return df
