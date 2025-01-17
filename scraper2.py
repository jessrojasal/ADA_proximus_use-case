import pandas as pd
from googleapiclient.discovery import build
import time
import json
import os

# Load credentials from a JSON file
def load_credentials(key_file: str = "google_api_key.json"):
    """
    Loads the Google API key and CSE ID from the specified JSON file.

    :param key_file: Path to the JSON file containing the credentials.
    :return: A tuple containing the API_KEY and CSE_ID.
    :raises FileNotFoundError: If the configuration file is not found.
    :raises KeyError: If the API_KEY or CSE_ID is missing in the configuration file.
    """
    if os.path.exists(key_file):
        with open(key_file, "r") as file:
            credentials = json.load(file)
            API_KEY = credentials.get("API_KEY")
            CSE_ID = credentials.get("CSE_ID")
            if not API_KEY or not CSE_ID:
                raise KeyError("API_KEY or CSE_ID is missing in the configuration file.")
            return API_KEY, CSE_ID
    else:
        raise FileNotFoundError(f"Configuration file '{key_file}' not found.")

# Set up Google Custom Search API
def google_search(query, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=query, cx=cse_id, **kwargs).execute()
    return res

def get_linkedin_profile(name, last_name, api_key, cse_id):
    query = f"{name} {last_name} AND proximus site:linkedin.com/in"
    try:
        # Perform the Google search using the Custom Search API
        results = google_search(query, api_key, cse_id, num=1)
        items = results.get("items", [])
        
        if items:
            for item in items:
                url = item.get("link")
                if "linkedin.com/in" in url:
                    return url
        return None
    except Exception as e:
        print(f"Error during search: {e}")
        return None

def process_data(input_file: str = "Scraper_test.csv"):
    API_KEY, CSE_ID = load_credentials("google_api_key.json")
    
    data = pd.read_csv(input_file)
    
    # Add a new column for LinkedIn URLs
    data["LinkedIn_URL"] = None
    
    # Perform search for each row and extract LinkedIn profile URL
    for index, row in data.iterrows():
        print(f"Searching for {row['name']} {row['last_name']}...")
        linkedin_url = get_linkedin_profile(row['name'], row['last_name'], API_KEY, CSE_ID)
        data.at[index, "LinkedIn_URL"] = linkedin_url
        
        time.sleep(1)
    
    print(data)
    data.to_csv(input_file, index=False)
    print(f"Updated CSV saved to {input_file}")

if __name__ == "__main__":
    process_data()  