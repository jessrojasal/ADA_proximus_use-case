import google.generativeai as genai
from utils.prompt import Prompt

class PhishingTarget:
    def __init__(self, data, model):
        self.data = data
        self.model = model

    def generate_email(self):
        """
        Generates an email for every given user details
        """
        print(f"Generating email for {self.data['name']}")
        user_prompt = Prompt(
            self.model, self.data["name"], self.data["last name"], self.data["position"]
        )
        prompt = user_prompt.get_prompt_baw()

        # Generate the email body content and use that to generate the subject and add HTML tags
        body = self.model.generate_content(prompt)
        html_prompt = user_prompt.generate_html_tags(body.text)
        html_body = self.model.generate_content(html_prompt)
        subject = self.model.generate_content(
            "Write me the subject of this email:\n" + body.text
        )

        self.data["HTMLBody"] = html_body.text
        self.data["Subject"] = subject.text
        # print(self.data)
