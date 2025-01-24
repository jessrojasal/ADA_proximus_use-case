import csv, json
from gophish import Gophish
from gophish.models import Group, User, Template, Campaign

API_KEY = "de15a463fccdf2bcede8c18d31f1643c638c87932b3881efde9e5a795b06ad17"
BASE_URL = "https://13.61.9.36:3333/"  # Change port and URL as needed
api = Gophish(API_KEY, host=BASE_URL, verify=False)  # Set verify=True for SSL

def json_generator(file_name):
    print('The imnput to the gophish main loop is assumed to be a json file')
    print('filename is: ', file_name)
    with open(file_name, 'r') as file:
        data = json.load(file)
        for entry in data:
            yield entry['email'], entry['subject'], entry['body']

def csv_generator(file_path):
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row if present
        for row in csv_reader:
            print('row in csv_generator function:', row)
            email, subject, body = row
            yield email, subject, body

def create_group(first_name, last_name, email):
	group = Group(
		name = first_name + last_name,
		targets=[User(first_name=first_name, last_name=last_name, email=email)]
	)
	created_group = api.groups.post(group)
	return [created_group]

def create_template(name, body):
	template = Template(name=name, html=body)
	template = api.templates.post(template)
	return template

def create_campaign(name, group, page, template, profile):
    campaign = Campaign(name=name, groups=group, page=page,
    template=template, smtp=profile)
    return api.campaigns.post(campaign)

def get_landing():
	landing_page_name = "TestPage"
	landing_pages = api.pages.get()
	return next((lp for lp in landing_pages if lp.name == landing_page_name), None)

def create_campaigns(input_file):
    # Fetch the landing page object
    landing_page = get_landing() 
    print(f"Using Landing Page: {landing_page.name}")

    # TODO make get_sending_profile function
    smtp_profiles = api.smtp.get()
    smtp_profile = smtp_profiles[0]  # Choose the SMTP profile you want to use
    print(f"Using SMTP Profile: {smtp_profile.name}, Host: {smtp_profile.host}")

    for email, subject, body in json_generator(input_file):
        try:
            print(f"Email: {email}, Subject: {subject}")
            groups = create_group('Test', 'Name', email)
            template = create_template('TestTemplateName', body)
            campaign = create_campaign('TestCampaignName', groups, landing_page, template, smtp_profile)
            print('Full csv file read. All campaigns made.')
        except Exception as e:
            print(f"[-] Error creating template for {email}: {e}")
            continue


if __name__ == '__main__':
    create_campaigns('../data/emails_output.csv')
