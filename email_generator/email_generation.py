import csv
from utils.target import PhishingTarget
from utils.genai import GenAI
import json

def process_csv_and_generate_emails(model, csv_file, output_file):
    with open(csv_file, mode="r") as file:
        csv_reader = csv.DictReader(file)
        rows_as_dicts = []
        for row in csv_reader:
            rows_as_dicts.append(row)
    out_data = []
    for row in rows_as_dicts:
        mytarget = PhishingTarget(row, model)
        mytarget.generate_email(topic="Microsoft")
        out_data.append(mytarget.data)

    with open(output_file, "w") as outfile:
        json.dump(out_data, outfile, indent=4)
    print(f"Emails saved to {output_file}")

genai = GenAI(keyfile="key.json")
genai.initialize_genai()

process_csv_and_generate_emails(
    genai.model,
    csv_file="../data/targets.csv",
    output_file="../data/emails_output.json",
)