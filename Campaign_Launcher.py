from gophish import Gophish
from gophish.models import Group, User, Template, Campaign


# Configure your Gophish credentials
API_KEY = "b953f2d2a428582b9457ff928ae612d8a640ce87b542ff59a584c4e7b7409180"
API_HOST = "http://94.110.206.175:3333/"
VERIFY_SSL = False

client = Gophish(api_key=API_KEY, host=API_HOST, verify=VERIFY_SSL)

# Retrieve the SMTP profile
smtp_profiles = client.smtp.get()
default_smtp_id = smtp_profiles[0]
print(f"Using SMTP profile: {smtp_profiles[0].name} (ID: {default_smtp_id})")

# Retrieve the first landing page
landing_pages = client.pages.get()
default_page_id = landing_pages[0]
print(f"Using Landing Page: {landing_pages[0].name} (ID: {default_page_id})")


# Read your target info from a CSV or text file
input_file = "targets.csv"
with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Loop over each person and create Template, Group, Campaign
for line in lines:
    line = line.strip()
    if not line or ";" not in line:
        continue

    first_name, last_name, email = line.split(";")

    # Create a unique Template for each person
    template_name = f"Template for {first_name} {last_name}"
    new_template = Template(
        name=template_name,
        subject="Phishing Test",
        from_address="no-reply@example.com",
        html=(
            f"<html><body>"
            f"<h2>Hello {first_name} {last_name},</h2>"
            f"<p>This is a personalized phishing simulation test.</p>"
            f"</body></html>"
        )
    )

    try:
        created_template = client.templates.post(new_template)
        print(f"[+] Created Template: {created_template.name} (ID: {created_template.id})")
    except Exception as e:
        print(f"[-] Error creating template for {first_name} {last_name}: {e}")
        continue

    # Create a unique Group (with just one user) for each person
    group_name = f"Group for {first_name} {last_name}"
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email
    )
    new_group = Group(name=group_name, targets=[user])

    try:
        created_group = client.groups.post(new_group)
        print(f"[+] Created Group: {created_group.name} (ID: {created_group.id})")
    except Exception as e:
        print(f"[-] Error creating group for {first_name} {last_name}: {e}")
        continue

    # Create a Campaign for this single user
    campaign_name = f"Campaign for {first_name} {last_name}"
    campaign = Campaign(
        name=campaign_name,
        template=created_template,
        page=default_page_id,
        smtp=default_smtp_id,
        groups=[created_group],
        url="http://your-phishing-server.com" 
    )

    try:
        created_campaign = client.campaigns.post(campaign)
        print(f"[+] Created Campaign: {created_campaign.name} (ID: {created_campaign.id})\n")
    except Exception as e:
        print(f"[-] Error creating campaign for {first_name} {last_name}: {e}")
        continue