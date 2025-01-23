from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import time
import json
import os
from scraper.path import LINKEDIN_CREDENTIALS_FILE, LINKEDIN_COOKIES_FILE

def launch_browser():
    """Launch a WebDriver for Chrome or Firefox automatically.
    Use Chrome as first option; if it fails use Firefox.
    
    :return: Selenium WebDriver instance.
    """
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        #driver_service = ChromeService(ChromeDriverManager().install())
        print("Launching Chrome...")
        return webdriver.Chrome(options=options)
    except Exception as e:
        print(f"Failed to launch Chrome. Error: {e}")
        try:
            options = webdriver.FirefoxOptions()
            options.add_argument("--headless")
            options.binary_location = "/usr/bin/firefox"
            
            #driver_service = FirefoxService(GeckoDriverManager().install())
            print("Launching Firefox...")
            service = FirefoxService("/usr/local/bin/geckodriver")
            return webdriver.Firefox(service=service, options=options)
        except Exception as e:
            print(f"Failed to launch Firefox. Error: {e}")
            raise Exception("Both Chrome and Firefox failed to launch. Please check your setup.")

def linkedin_login(driver):
    """Handle LinkedIn login using cookies or credentials.
    
    :param driver: Selenium WebDriver instance.
    """
    def login_to_linkedin():
        """Automate LinkedIn login using credentials from a JSON file."""
        if os.path.exists(LINKEDIN_CREDENTIALS_FILE):
            with open(LINKEDIN_CREDENTIALS_FILE, "r") as file:
                config = json.load(file)
                email = config.get("email")
                password = config.get("password")
                if not email or not password:
                    raise ValueError("Email or password is missing in the configuration file.")
        else:
            raise FileNotFoundError(f"Configuration file '{LINKEDIN_CREDENTIALS_FILE}' not found.")

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

        if "feed" in driver.current_url:
            print("Login successful!")
        else:
            raise Exception("Login failed. Check your credentials.")

    def save_cookies():
        """Save cookies from the Selenium browser session to a JSON file."""
        cookies = driver.get_cookies()
        with open(LINKEDIN_COOKIES_FILE, "w") as file:
            json.dump(cookies, file)
        print(f"Cookies saved to {LINKEDIN_COOKIES_FILE}")

    def load_cookies():
        """Load cookies from a JSON file and add them to the Selenium browser session."""
        if os.path.exists(LINKEDIN_COOKIES_FILE):
            with open(LINKEDIN_COOKIES_FILE, "r") as file:
                cookies = json.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
            print(f"Cookies loaded from {LINKEDIN_COOKIES_FILE}")
        else:
            raise FileNotFoundError(f"Cookies file '{LINKEDIN_COOKIES_FILE}' not found.")

    def login_with_cookies():
        """Login to LinkedIn by loading cookies into the browser."""
        driver.get("https://www.linkedin.com")
        time.sleep(3)
        
        try:
            load_cookies()
            driver.refresh()
            time.sleep(3)
            if "feed" in driver.current_url:
                print("Logged in using cookies!")
                return True
            else:
                print("Cookies might have expired. Need to log in again.")
                return False
        except FileNotFoundError:
            print("Cookies file not found, logging in with credentials.")
            return False

    # First attempt to log in with cookies 
    # If cookies expired or missing, log in with credentials and save cookies
    if not login_with_cookies():
        try:
            login_to_linkedin()
            save_cookies()
        finally:
            driver.quit()
