import os
from dotenv import load_dotenv

load_dotenv()

# Centralized settings
API_KEY = os.getenv("API_KEY") # api key for the gophish API
API_URL = os.getenv("API_URL") #url for the gophish API
GEMINI_KEY = os.getenv("GEMINI_KEY")
