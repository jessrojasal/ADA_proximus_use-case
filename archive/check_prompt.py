from email_generator.email_generation import process_csv_and_generate_emails

output_file, targets_file, model_key = './data/output.csv', './data/targets.csv', './key.json'
process_csv_and_generate_emails(output_file, targets_file, model_key)