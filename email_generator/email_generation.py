import google.generativeai as genai # type: ignore
import pandas as pd
import json
import os
from utils.prompt import Prompt 

def initialize_genai(key_file: str = "key.json"):
    """
    Initializes the Google Generative AI model using an API key stored in config.json file.

    :param config_file: A string that represents the path to the config.json file.
    :return: An instance of the initialized generative model (genai.GenerativeModel).
    :raises FileNotFoundError: If the configuration file is not found.
    :raises KeyError: If the "GEMINI_API_KEY" is missing in the configuration file.
    """
    if os.path.exists(key_file):
        with open(key_file, "r") as file:
            key = json.load(file)
            GEMINI_API_KEY = key.get("GEMINI_API_KEY")
            if not GEMINI_API_KEY:
                raise KeyError("GEMINI_API_KEY is missing in the configuration file.")
    else:
        raise FileNotFoundError(f"Configuration file '{key_file}' not found.")

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    return model

def generate_email(model, name, lastname, position):
    """
    Generates an email for every given user details
    :return: Email subject and body
    """
    user_prompt = Prompt(model, name, lastname, position)
    prompt = user_prompt.get_prompt_baw()

    # Generate the email body content
    body = model.generate_content(prompt)
    #print(body.text)

    # Generate the email subject
    subject = model.generate_content("Write me the subject of this email:\n"+body.text)
    #print(subject.text)

    # Return the subject and body
    return subject.text, body.text


def process_csv_and_generate_emails(csv_file, model, output_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Create a list to store email data
    emails_data = []

    # Loop through each row and generate an email
    for index, row in df.iterrows():
        email = row['email']
        name = row['name']
        lastname = row['last name']
        position = row['position']
        
        # Generate the phishing email
        subject, body = generate_email(model, name, lastname, position)
        print()
        # Append the email data to the list
        emails_data.append({
            "name": name,
            "lastname": lastname,
            "email": email,
            "subject": subject,
            "body": body
        })
        #print(emails_data)
    # Create a DataFrame from the emails data
    output_df = pd.DataFrame(emails_data)
    # Save the DataFrame to a CSV file
    output_df.to_csv(output_file, index=False)
    print(f"Emails saved to {output_file}")

# Initialize the model
model = initialize_genai()

# Process the CSV and generate emails
csv_file = '../data/targets.csv'
process_csv_and_generate_emails(csv_file, model, output_file="../data/emails_output.csv")