import google.generativeai as genai
import os
import json

class GenAI:
    def __init__(self, keyfile="key.json"):
        self.model = None
        self.key_file = keyfile

    def initialize_genai(self):
        """
        Initializes the Google Generative AI model using an API key stored in config.json file.

        :param config_file: A string that represents the path to the config.json file.
        :return: An instance of the initialized generative model (genai.GenerativeModel).
        :raises FileNotFoundError: If the configuration file is not found.
        :raises KeyError: If the "GEMINI_API_KEY" is missing in the configuration file.
        """
        if os.path.exists(self.key_file):
            with open(self.key_file, "r") as file:
                key = json.load(file)
                GEMINI_API_KEY = key.get("GEMINI_API_KEY")
                if not GEMINI_API_KEY:
                    raise KeyError(
                        "GEMINI_API_KEY is missing in the configuration file."
                    )
        else:
            raise FileNotFoundError(f"Configuration file '{key_file}' not found.")

        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-pro")
