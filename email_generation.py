import google.generativeai as genai # type: ignore
import pandas as pd
import json
import os
import random

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

def generate_email(model, name, lastname, teamname, businessunit):

    # Phishing parameters microsoft
    phishing_parameters_microsoft = [
    {"Details": "Try the new Microsoft AI-powered assistant. Priority access for your business unit", 
        "Fake Link": "https://example.com/secure-login", 
        "Created By": "Sam Sussy", 
        "Position": "IT Support Specialist",
        "Reason": "New AI-powered assistant"},
    
    {"Details": "Your business unit is changing Microsoft Office License. Will Expire Soon", 
        "Fake Link": "https://example.com/reset-password", 
        "Created By": "Sally Sneaky", 
        "Position": "License Management Specialist", 
        "Reason": "Office License Expiry"},
    
    {"Details": "Exclusive Training Webinar on New Tools", 
        "Fake Link": "https://example.com/join-webinar", 
        "Created By": "Richard Rascal", 
        "Position": "Training Coordinator", 
        "Reason": "Webinar Invitation"},
    
    {"Details": "Email Storage Full. Please clear space immediately", 
        "Fake Link": "https://example.com/manage-storage", 
        "Created By": "Bernard Bandit", 
        "Position": "System Administrator", 
        "Reason": "Email Storage Full"}
    ]

    random_pick = random.choice(phishing_parameters_microsoft)

    # Formulate a prompt
    prompt = f'''Write an email from {random_pick["Created By"]}, a {random_pick["Position"]}, to {name} {lastname}, a member of the {teamname} team in the {businessunit} business unit. 
    The email should convey the following message: 
    {random_pick["Details"]}. 
    Ensure the tone is professional and polite, with clear instructions for {name} to click on this link: {random_pick["Fake Link"]}. 
    The subject should reflect the importance of the matter but without urgency, maintaining a formal and courteous approach. 
    Only write the body of this email, including a professional signature from {random_pick["Position"]}.'''

    # Generate the email body content
    body = model.generate_content(prompt)
    print(body.text)

    # Generate the email subject
    subject = model.generate_content("Write me the subject of this email:\n"+body.text)
    print(subject.text)

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
        teamname = row['team name']
        businessunit = row['business unit']

        # Generate the phishing email
        subject, body = generate_email(model, name, lastname, teamname, businessunit)

        # Append the email data to the list
        emails_data.append({
            "email": email,
            "subject": subject,
            "body": body
        })

    # Create a DataFrame from the emails data
    output_df = pd.DataFrame(emails_data)

    # Save the DataFrame to a CSV file
    output_df.to_csv(output_file, index=False)

    print(f"Emails saved to {output_file}")

# Initialize the model
model = initialize_genai()

# Process the CSV and generate emails
csv_file = 'test.csv'
process_csv_and_generate_emails(csv_file, model, output_file="emails_output.csv")


