import random

class Prompt:
    def __init__(self, model, name, lastname, position):
        self.name = name
        self.lastname = lastname
        self.position = position
        self.model = model

    def get_prompt_microsoft(self):
        phishing_parameters_microsoft = [
            {
                "Details": "Try the new Microsoft AI-powered assistant. Priority access for your business unit",
                "Fake Link": "https://example.com/secure-login",
                "Created By": "Sam Sussy",
                "Position": "IT Support Specialist",
                "Reason": "New AI-powered assistant",
            },
            {
                "Details": "Your business unit is changing Microsoft Office License. Will Expire Soon",
                "Fake Link": "https://example.com/reset-password",
                "Created By": "Sally Sneaky",
                "Position": "License Management Specialist",
                "Reason": "Office License Expiry",
            },
            {
                "Details": "Exclusive Training Webinar on New Tools",
                "Fake Link": "https://example.com/join-webinar",
                "Created By": "Richard Rascal",
                "Position": "Training Coordinator",
                "Reason": "Webinar Invitation",
            },
            {
                "Details": "Email Storage Full. Please clear space immediately",
                "Fake Link": "https://example.com/manage-storage",
                "Created By": "Bernard Bandit",
                "Position": "System Administrator",
                "Reason": "Email Storage Full",
            },
        ]
        random_pick = random.choice(phishing_parameters_microsoft)

        prompt = f"""Write an email from {random_pick["Created By"]}, a {random_pick["Position"]}, to {self.name} {self.lastname}, a {self.position} in Proximus. 
        The email should convey the following message: {random_pick["Details"]}. 
        Ensure the tone is professional and polite, with clear instructions for {self.name} to click on this link: {random_pick["Fake Link"]}. 
        The subject should reflect the importance of the matter but without urgency, maintaining a formal and courteous approach. 
        Write the body of the email including HTML tags so that it is well-structured and ready to use in an email client.
        Provide only the raw HTML code as output. Do not use backticks,
        The href tag for the link should read Click here. 
        End with a professional signature from {random_pick["Position"]}."""
        return prompt

    def get_prompt_baw(self):
        phishing_examples = [
            {
                "Reason": "Tickets to the Grotte De Han caves",
                "Fake Link": "https://example.com/secure-login",
                "Created By": "Nicole Hoelyarts",
            },
            {
                "Reason": "10% off in IKEA",
                "Fake Link": "https://example.com/reset-password",
                "Created By": "Line Dalemans",
            },
            {
                "Reason": "Kerefel 10% on select appliances",
                "Fake Link": "https://example.com/join-webinar",
                "Created By": "Dirk Verbiest",
            },
            {
                "Reason": "15% discount on SVEA SOLAR panels",
                "Fake Link": "https://example.com/join-webinar",
                "Created By": "Dirk Verbiest",
            },
        ]
        random_pick = random.choice(phishing_examples)
        prompt = f"""You are a hacker trying to phish people at Proximus.
        Write a 5-6 lines email which looks legitimate from {random_pick["Created By"]}, a Marketing Manager from the organisation 
        Benefits at Work to {self.name} {self.lastname} who is a {self.position} in the company on the following theme: 
        {random_pick["Reason"]} as they are a member of Benefits at work program. 
        Instruct them politely to click the button in the email to proceed with the login to access the benefits 
        Do not specify any dates or time periods. 
        Only write the body of this email."""
        return prompt

    def generate_html_tags(self, body, click_button_tag):
        prompt = f"""This is content of an email. {body} Add appropriate html tags so that it is well-structured and ready to use in an email client.
        Provide only the raw HTML code as output and do not use backticks in the begining. 
        Start with a <h3> tag for the salutation followed by appropriate <p> tags.
        Set the button to click within <div class="button-container"> with the text {click_button_tag} and the link as http://94.110.206.175:5000/landing"""
        return prompt