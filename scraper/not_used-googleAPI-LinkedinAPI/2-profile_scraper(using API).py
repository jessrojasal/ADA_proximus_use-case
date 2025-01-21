import requests
import pandas as pd
import json
import os

# Example function to load cookies and get the necessary headers
def load_cookies():
    # Replace with your actual cookies and Authorization token (you need to extract these)
    cookies = {
        "li_at": "your_authentication_cookie",
        "JSESSIONID": "your_jsessionid_cookie"
    }
    headers = {
        "Authorization": "Bearer YOUR_ACCESS_TOKEN",  # Use the actual token here
        "x-restli-protocol-version": "2.0.0",
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    }
    return cookies, headers

# Function to scrape LinkedIn profile using Voyager API
def scrape_linkedin_profile_via_voyager(profile_url, cookies, headers):
    # Extract the profile ID from the URL (you may need to parse it based on the URL structure)
    profile_id = profile_url.split("/")[-2]
    api_url = f"https://www.linkedin.com/voyager/api/identity/profiles/{profile_id}"

    response = requests.get(api_url, headers=headers, cookies=cookies)
    
    if response.status_code == 200:
        data = response.json()
        
        # Extract relevant data from the response JSON (example structure)
        profile_data = {
            'url': profile_url,
            'about': data.get('about', ''),
            'experience': data.get('experience', ''),
            'education': data.get('education', '')
        }
        return profile_data
    else:
        print(f"Error fetching data for {profile_url}: {response.status_code}")
        return None

# Main function to scrape multiple profiles
def main(df):
    # Load cookies and headers for API requests
    cookies, headers = load_cookies()

    # List to hold scraped data
    scraped_data = []

    for index, row in df.iterrows():
        profile_url = row['linkedin_profile']
        print(f"Scraping profile: {profile_url}")
        profile_data = scrape_linkedin_profile_via_voyager(profile_url, cookies, headers)
        if profile_data:
            scraped_data.append(profile_data)

    # Convert results to DataFrame
    profile_df = pd.DataFrame(scraped_data)

    return profile_df

# Main code to load the CSV, scrape, and save the results
try:
    # Load your CSV file
    csv_file = os.path.join(os.getcwd(), "scraper", "Scraper_test.csv")    
    df = pd.read_csv(csv_file)
    
    # Check if 'linkedin_profile' column exists
    if 'linkedin_profile' not in df.columns:
        raise KeyError("'linkedin_profile' column is missing in the CSV file")

    # Scrape the profiles and store the results in a new DataFrame
    result_df = main(df)

    # Save the result to a new CSV file
    result_csv_file = os.path.join(os.getcwd(), "scraper", "scraped_linkedin_data_voyager.csv")
    result_df.to_csv(result_csv_file, index=False)
    print(f"Scraped data saved to {result_csv_file}")

except Exception as e:
    print(f"An error occurred: {e}")


 