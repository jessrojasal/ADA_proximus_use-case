from scraper.login import linkedin_login, launch_browser
from scraper.linkedin_urls import get_linkedin_url
from scraper.profile_content import get_profile_content
import csv
import os

def scraper(csv_file):
    try:
        # Load CSV file
        file = open(csv_file, mode="r")
        df = csv.reader(file) 

        # Launch browser and log in
        driver = launch_browser()  
        linkedin_login(driver) 

        # Get LinkedIn profile url for each person
        updated_df = get_linkedin_url(df, driver)

        # Get text from each profile in the DataFrame
        if 'linkedin_profile' in updated_df.columns:
            updated_df = get_profile_content(updated_df, driver)

        # Save the updated DataFrame to a new CSV file
        scraped_info_file = os.path.join(os.getcwd(), "data", "scraped_targets.csv")
        updated_df.to_csv(scraped_info_file, index=False)

    except Exception as e:
        pass

    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    scraper()
