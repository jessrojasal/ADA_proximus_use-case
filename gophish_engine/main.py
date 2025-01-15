from gophish.models import Campaign
from gophish.models import Group, User
from gophish import *
from gophish.models import Template

# Replace with your API key and URL of your GoPhish instance
API_KEY = "b953f2d2a428582b9457ff928ae612d8a640ce87b542ff59a584c4e7b7409180"
BASE_URL = "http://94.110.206.175:3333/"  # Change port and URL as needed

# Connect to GoPhish
api = Gophish(API_KEY, host=BASE_URL, verify=False)  # Set verify=True for SSL

# Fetch the email template object
templates = api.templates.get()
template = templates[0]  # Choose the template you want to use
print(f"Using Template: {template.name}, Subject: {template.subject}")

# Fetch the landing page object
landing_pages = api.pages.get()
landing_page = landing_pages[0]  # Choose the landing page you want to use
print(f"Using Landing Page: {landing_page.name}")

# Fetch the SMTP profile object
smtp_profiles = api.smtp.get()
smtp_profile = smtp_profiles[0]  # Choose the SMTP profile you want to use
print(f"Using SMTP Profile: {smtp_profile.name}, Host: {smtp_profile.host}")

# Fetch the group object
groups = api.groups.get()
group = groups[0]  # Choose the group you want to use
print(f"Using Group: {group.name}, Number of Users: {len(group.targets)}")

# Define the campaign
campaign = Campaign(
    name="Daily Phishing Campaign",
    template=template,# Correct template ID here
    page=landing_page,
    smtp=smtp_profile,  # Correct sending profile ID here
    url="http://your-phishing-server.com",  # Your phishing server URL
    groups=[group]  # Group with recipients
)

# Create the campaign
try:
    response = api.campaigns.post(campaign)
    print(f"Campaign created successfully! ID: {response.id}")
except Exception as e:
    print(f"Error creating campaign: {e}")
