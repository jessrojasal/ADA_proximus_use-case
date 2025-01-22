from gophish.models import Campaign
from gophish.models import Group, User
from gophish import *
from gophish.models import Template

# Replace with your API key and URL of your GoPhish instance
API_KEY = "b953f2d2a428582b9457ff928ae612d8a640ce87b542ff59a584c4e7b7409180"
BASE_URL = "http://94.110.206.175:3333/"
VERIFY_SSL = False

client = Gophish(api_key=API_KEY, host=BASE_URL, verify=VERIFY_SSL)

# 1. Delete all campaigns
campaigns = client.campaigns.get()
for campaign in campaigns:
    try:
        client.campaigns.delete(campaign.id)
        print(f"[+] Deleted Campaign: {campaign.name} (ID: {campaign.id})")
    except Exception as e:
        print(f"[-] Error deleting campaign {campaign.name} (ID: {campaign.id}): {e}")

# 2. Delete all groups
groups = client.groups.get()
for group in groups:
    try:
        client.groups.delete(group.id)
        print(f"[+] Deleted Group: {group.name} (ID: {group.id})")
    except Exception as e:
        print(f"[-] Error deleting group {group.name} (ID: {group.id}): {e}")

# 3. Delete all templates
templates = client.templates.get()
for template in templates:
    try:
        client.templates.delete(template.id)
        print(f"[+] Deleted Template: {template.name} (ID: {template.id})")
    except Exception as e:
        print(f"[-] Error deleting template {template.name} (ID: {template.id}): {e}")
