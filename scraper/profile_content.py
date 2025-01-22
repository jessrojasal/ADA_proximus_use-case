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

def get_profile_content(data, driver):
    """
    Add extracted text from LinkedIn profiles to each dictionary in the list.
    
    :param data: List of dictionaries containing LinkedIn profile URLs.
    :param driver: Selenium WebDriver instance.
    :return: Updated list of dictionaries with profile text added.
    """
    target_sections = [
        "About",
        "Experience",
        "Education",
        "Licenses & certifications",
        "Volunteering",
        "Skills",
        "Courses",
        "Honors & awards",
        "Languages",
    ]

    for person in data:
        profile_url = person.get("linkedin_profile")
        if not profile_url:
            print(f"No LinkedIn profile URL found for {person['name']} {person['last_name']}. Skipping.")
            continue

        try:
            print(f"Scraping profile for {person['name']} {person['last_name']} at {profile_url}...")
            profile_data = scrape_text_from_profile(driver, profile_url)

            # Add extracted sections to the person's dictionary
            for section, text in profile_data.items():
                first_word = text.split("\n", 1)[0] if text else ""
                if first_word in target_sections:
                    person[first_word] = text
        except Exception as e:
            print(f"Error scraping {profile_url}: {e}")
            person["error"] = str(e)

    return data


