import pandas as pd
import time
from bs4 import BeautifulSoup  

def scrape_text_from_profile(driver, profile_url):
    """
    Extract text from specific sections of a LinkedIn profile page.

    :param driver: Selenium WebDriver instance.
    :param profile_url: LinkedIn profile URL.
    :return: A dictionary containing text from each section.
    """
    driver.get(profile_url)
    time.sleep(5)

    html_content = driver.page_source
    soup = BeautifulSoup(html_content, "html.parser")

    profile_data = {}

    # Loop through sections and extract text
    sections = soup.find_all("section")  
    for idx, section in enumerate(sections, start=1):
        try:
            # Extract all text
            section_text = section.get_text(separator="\n", strip=True)

            if section_text:
                paragraphs = section_text.split("\n")  
                unique_paragraphs = []
                last_paragraph = "" 

                # Loop through paragraphs and keep only unique ones
                for paragraph in paragraphs:
                    if paragraph and paragraph != last_paragraph: 
                        unique_paragraphs.append(paragraph)
                        last_paragraph = paragraph

                # Store text with no consecutive duplicates
                profile_data[f"section_{idx}"] = "\n".join(unique_paragraphs)

        except Exception as e:
            print(f"Error extracting section {idx}: {e}")
            profile_data[f"section_{idx}"] = None

    return profile_data

def get_profile_content(df, driver):
    """
    Add extracted text from LinkedIn profiles to the DataFrame.

    :param df: DataFrame containing a column with LinkedIn profile URLs.
    :param driver: Selenium WebDriver instance.
    :return: Updated DataFrame with profile text.
    """

    # Define the target sections
    target_sections = [
        "About",
        "Experience",
        "Education",
        "Licenses & certifications",
        "Volunteering",
        "Skills",
        "Courses",
        "Honors & awards",
        "Languages"
    ]
    

    for section in target_sections:
        df[section] = None  

    for index, row in df.iterrows():
        profile_url = row.get('linkedin_profile')

        if pd.notna(profile_url):  
            print(f"Scraping profile: {profile_url}")
            try:
                profile_data = scrape_text_from_profile(driver, profile_url)

                # Check the extracted data and add to appropriate columns
                for section, text in profile_data.items():
                    first_word = text.split("\n", 1)[0] if text else ""
                    
                    if first_word in target_sections:
                        df.at[index, first_word] = text

            except Exception as e:
                print(f"Error scraping {profile_url}: {e}")

    return df


