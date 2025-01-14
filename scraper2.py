import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import re

# Search in Google and fetch the LinkedIn URL
def google_search(name, last_name):
    query = f'site:linkedin.com/in "{name} {last_name}" AND Proximus'
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()  
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find all <a> tags with jsname="UWckNb"
        links = soup.find_all('a', jsname="UWckNb")

        for link in links:
            h3_tag = link.find('h3', class_="LC20lb MBeuO DKV0Md")
            if h3_tag:
                h3_text = h3_tag.text.strip()  
                full_name = re.sub(r'\s+', ' ', f"{name} {last_name}".strip())   
                if full_name.lower() in h3_text.lower():  
                    linkedin_url = link['href']
                    print(f"Found LinkedIn URL: {linkedin_url} for {full_name}")
                    return linkedin_url
            else:
                print(f"No <h3> tag found in the link: {link}")

    except Exception as e:
        print(f"Error for {name} {last_name}: {e}")
    return None

# Load DataFrame 
df = pd.read_csv('Scraper_test.csv')

# Add new column to store the LinkedIn URLs
df['linkedin_url'] = None

# Loop through the DF and search for each person
for index, row in df.iterrows():
    name = row['name']
    last_name = row['last_name']
    
    url = google_search(name, last_name)
    df.at[index, 'linkedin_url'] = url
    print(f"Processed: {name} {last_name}, URL: {url}")
    
    time.sleep(2)  

# Print the updated DF
print(df)
