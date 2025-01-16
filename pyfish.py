import csv
from gophish import Gophish
from gophish.models import Group, User, Template, Campaign

API_KEY = "b953f2d2a428582b9457ff928ae612d8a640ce87b542ff59a584c4e7b7409180"
BASE_URL = "http://94.110.206.175:3333/"  # Change port and URL as needed
api = Gophish(API_KEY, host=BASE_URL, verify=False)  # Set verify=True for SSL



def csv_generator(file_path):
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row if present
        for row in csv_reader:
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


if __name__ == '__main__':
    file_path = 'emails_output.csv'

    # Fetch the landing page object
    landing_page = get_landing() 
    print(f"Using Landing Page: {landing_page.name}")

    # TODO make get_sending_profile function
    smtp_profiles = api.smtp.get()
    smtp_profile = smtp_profiles[0]  # Choose the SMTP profile you want to use
    print(f"Using SMTP Profile: {smtp_profile.name}, Host: {smtp_profile.host}")

    for email, subject, body in csv_generator(file_path):
        try:
            print(f"Email: {email}, Subject: {subject}")
            groups = create_group('Test', 'Name', email)
            template = create_template('TestTemplateName', body)
            campaign = create_campaign('TestCampaignName', groups, landing_page, template, smtp_profile)
            print('Full csv file read. All campaigns made.')
        except Exception as e:
            print(f"[-] Error creating template for {email}: {e}")
            continue
