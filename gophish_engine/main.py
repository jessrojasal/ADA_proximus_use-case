from gophish.models import Group, User
from gophish import Gophish

# Replace with your API key and URL of your GoPhish instance
API_KEY = "your_api_key"
BASE_URL = "http://localhost:3333"  # Change port and URL as needed

# Connect to GoPhish
api = Gophish(API_KEY, host=BASE_URL, verify=False)  # Set verify=True for SSL


# Create a new group
group = Group(
    name="Test Group",
    targets=[
        User(first_name="John", last_name="Doe", email="john.doe@example.com"),
        User(first_name="Jane", last_name="Smith", email="jane.smith@example.com")
    ]
)

# Save the group
created_group = api.groups.post(group)
print(f"Group Created: {created_group.name}, ID: {created_group.id}")

