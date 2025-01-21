from login import linkedin_login, launch_browser
from linkedin_urls import get_linkedin_url
from profile_content import get_profile_content
import pandas as pd
import os

try:
    # Load CSV file
    csv_file = os.path.join(os.getcwd(), "scraper", "Scraper_test.csv")
    df = pd.read_csv(csv_file)

    # Launch browser and log in
    driver = launch_browser()  
    linkedin_login(driver) 

    # Get LinkedIn profile url for each person
    updated_df = get_linkedin_url(df, driver)

    # Get text from each profile in the DataFrame
    if 'linkedin_profile' in updated_df.columns:
        updated_df = get_profile_content(updated_df, driver)
    else:
        print("No 'linkedin_profile' column found in the CSV file.")

    # Save the updated DataFrame back to the CSV file
    df.to_csv(csv_file, index=False)
    print("Updated CSV file saved.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if 'driver' in locals():
        driver.quit()
