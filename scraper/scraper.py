from login import linkedin_login, launch_browser
from linkedin_urls import get_linkedin_url
from profile_content import get_profile_content
import pandas as pd
import os

def scraper(csv_file = os.path.join(os.getcwd(), "scraper", "Scraper_test.csv")):
    try:
        # Load CSV file
        df = pd.read_csv(csv_file)

        # Launch browser and log in
        driver = launch_browser()  
        linkedin_login(driver) 

        # Get LinkedIn profile url for each person
        updated_df = get_linkedin_url(df, driver)

        # Get text from each profile in the DataFrame
        if 'linkedin_profile' in updated_df.columns:
            updated_df = get_profile_content(updated_df, driver)

        # Save the updated DataFrame to a new CSV file
        scraped_info_file = os.path.join(os.getcwd(), "scraper", "Scraped_info.csv")
        updated_df.to_csv(scraped_info_file, index=False)

    except Exception as e:
        pass

    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    scraper()