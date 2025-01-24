import csv
from .utils.target import PhishingTarget
import google.generativeai as genai
import os
import json
import time

# Main function to process CSV and generate emails for every target
def process_csv_and_generate_emails(output_file, targets_file, model_key ):
    model = initialize_genai(model_key)
 
    with open(targets_file, mode="r", newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file, quotechar='"')
        rows_as_dicts = []
        for row in csv_reader:
            rows_as_dicts.append(row)
    out_data = []
    print('Out data: ', out_data)

    for row in rows_as_dicts:
        print('row: ', row)
        mytarget = PhishingTarget(row, model)
        mytarget.generate_email(topic="Microsoft")
        out_data.append({"name":mytarget.data["name"],
                          "last name":mytarget.data["last_name"],
                          "email":mytarget.data["email"],
                          "position":mytarget.data["position"],
                          "body":mytarget.data["body"],
                          "subject":mytarget.data["subject"]})

    with open(output_file, "w") as outfile:
        json.dump(out_data, outfile, indent=4)
    print(f"Emails saved to {output_file}")

def initialize_genai(key_file):
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
                raise KeyError(
                    "GEMINI_API_KEY is missing in the configuration file."
                )
    else:
        raise FileNotFoundError(f"Configuration file '{key_file}' not found.")

    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel("gemini-pro")

if __name__ == "__main":
    process_csv_and_generate_emails(
        output_file='../data/output.csv', 
        targets_file='../data/scraped_targets.csv', 
        model_key='./key.json'
    )
