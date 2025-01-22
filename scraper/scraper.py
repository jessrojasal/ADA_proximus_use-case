from scraper.login import linkedin_login, launch_browser
from scraper.linkedin_urls import get_linkedin_urls
from scraper.profile_content import get_profile_content
import csv

def scraper(input_csv, output_csv):
    """
    Scrape LinkedIn profile data and save the updated data to a CSV file.

    :param input_csv: Path to the input CSV file.
    :param output_csv: Path to the output CSV file.
    """
    # Launch browser and log in
    driver = launch_browser()
    linkedin_login(driver)

    try:
        # Collect LinkedIn profile URLs
        linkedin_data = get_linkedin_urls(input_file=input_csv, driver=driver)

        # Process profiles to extract content
        updated_data = get_profile_content(linkedin_data, driver)

        # Save the updated data to a CSV file
        with open(output_csv, mode="w", newline="") as file:
            fieldnames = updated_data[0].keys() if updated_data else []
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(updated_data)

        print(f"Updated data has been saved to {output_csv}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
   scraper()
