import json
from gophish import Gophish
from gophish.models import Campaign, Group, User, Template, SMTP

# Replace these with your actual GoPhish API key and host URL
API_KEY = "b953f2d2a428582b9457ff928ae612d8a640ce87b542ff59a584c4e7b7409180"
API_HOST = "http://94.110.206.175:3333/"  # Change port and URL as needed

# Initialize the GoPhish API client
api = Gophish(API_KEY, host=API_HOST)

def read_json(file_path):
    """Reads the JSON file containing email data."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def create_group(email, first_name, last_name):
    """Creates a group with a single recipient."""
    group = Group(
        name=first_name + last_name,
        targets=[User(first_name=first_name, email=email)]
    )
    return api.groups.post(group)

def create_email_template(name, email_body):
    """Creates an email template."""
    template = Template(
        name=name,
        subject="Your Subject Here",  # Customize the subject
        html=email_body
    )
    return api.templates.post(template)

def get_smtp_profile():
    """Fetches an existing SMTP profile or creates one."""
    smtp_profiles = api.smtp.get()
    if smtp_profiles:
        return smtp_profiles[0]  # Return the first SMTP profile
    else:
        # Replace with your actual SMTP details
        smtp = SMTP(
            name="Default SMTP Profile",
            host="smtp.example.com",
            username="your_smtp_username",
            password="your_smtp_password",
            from_address="no-reply@example.com"
        )
        return api.smtp.post(smtp)

def create_campaign(name, group, landing_page, template, smtp):
    """Creates a campaign."""
    campaign = Campaign(
        name=name,
        groups=[group],
        page=landing_page,
        template=template,
        smtp=smtp,
        url="http://your-phishing-server-url"  # Replace with your phishing server URL
    )
    return api.campaigns.post(campaign)

def main():
    # Read the JSON file with email data
    json_file_path = 'emails.json'  # Replace with your JSON file path
    email_data = read_json(json_file_path)

    # Get the SMTP profile
    smtp_profile = get_smtp_profile()

    # Fetch or create a default landing page
    landing_pages = api.pages.get()
    landing_page = landing_pages[0] if landing_pages else None
    if not landing_page:
        print("No landing page found. Please create a landing page in the GoPhish dashboard.")
        return

    # Loop through the email data and create campaigns
    for entry in email_data:
        email = entry['email']
        email_body = entry['body']
        first_name = entry['name']
        last_name = entry['last name']

        print(f"Processing email: {email}")

        # Create a group for the email
        group = create_group(email, first_name, last_name)

        # Create an email template for the email
        template_name = f"Template for {email}"
        template = create_email_template(template_name, email_body)

        # Create the campaign
        campaign_name = f"Campaign for {email}"
        campaign = create_campaign(campaign_name, group, landing_page, template, smtp_profile)

        print(f"Campaign created: {campaign.name} (ID: {campaign.id})")

if __name__ == "__main__":
    main()
