from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from requests import Session
import time
import json
import os
import pandas as pd

def launch_browser():
    """Launch a new instance of the Chrome Webdriver"""
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    return webdriver.Chrome(options=options)

def login_to_linkedin(driver):
    """Automate LinkedIn login using credentials from a JSON file."""

    # Load credentials from the JSON file
    credentials_file = "linkedin_credentials.json"
    if os.path.exists(credentials_file):
        with open(credentials_file, "r") as file:
            config = json.load(file)
            email = config.get("email")
            password = config.get("password")
            if not email or not password:
                raise ValueError("Email or password is missing in the configuration file.")
    else:
        raise FileNotFoundError(f"Configuration file '{credentials_file}' not found.")

    # Navigate to LinkedIn login page
    url = 'https://www.linkedin.com/login'
    driver.get(url)
    time.sleep(3)

    username = driver.find_element(By.XPATH, "//input[@name='session_key']")
    password_field = driver.find_element(By.XPATH, "//input[@name='session_password']")

    username.send_keys(email)
    password_field.send_keys(password)
    time.sleep(3)

    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()
    time.sleep(3)

def search_person(driver, first_name, last_name):
    """
    Search for a person on LinkedIn and return their profile URL.
    
    Args:
        driver: Selenium WebDriver instance.
        first_name: First name of the person.
        last_name: Last name of the person.
    
    Returns:
        The LinkedIn profile URL of the person or None if not found.
    """
    search_url = 'https://www.linkedin.com/company/proximusgroup/people/'
    driver.get(search_url)
    time.sleep(4) 

    # Locate the search input field
    search_field = driver.find_element(By.XPATH, "//input[@id='people-search-keywords']")
    search_field.clear()
    search_field.send_keys(f"{first_name} {last_name}")
    search_field.send_keys(Keys.RETURN)
    time.sleep(4)  

    # Search for the specific person
    try:
        # Find all elements that contain profiles
        profiles = driver.find_elements(By.CSS_SELECTOR, ".org-people-profile-card__profile-info")
        
        for profile in profiles:
            # Locate the name container
            name_element = profile.find_element(By.CSS_SELECTOR, ".artdeco-entity-lockup__title div")
            name_text = name_element.text.strip()

            # If the name matches, get the profile link
            if name_text.lower() == f"{first_name.lower()} {last_name.lower()}":
                profile_link = profile.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                return profile_link
        
        # If no match is found
        return None
    
    except Exception as e:
        print(f"Error while searching for {first_name} {last_name}: {e}")
        return None

def update_dataframe_with_profiles(df, driver):
    """Add LinkedIn profile URLs to the DataFrame."""
    profile_urls = []

    for index, row in df.iterrows():
        first_name = row['name']
        last_name = row['last_name']
        print(f"Searching for {first_name} {last_name}...")

        profile_url = search_person(driver, first_name, last_name)
        profile_urls.append(profile_url)

    # Add the profile URL column to the DataFrame
    df['linkedin_profile'] = profile_urls
    return df

# Load your CSV file
csv_file = "Scraper_test.csv"  
df = pd.read_csv(csv_file)

# Launch the browser and log in to LinkedIn
driver = launch_browser()
login_to_linkedin(driver)

# Update the DF with LinkedIn URLs
updated_df = update_dataframe_with_profiles(df, driver)

# Print the updated DF
print(updated_df)
