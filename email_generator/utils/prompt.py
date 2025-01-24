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
                "Created By": "Sam Sussy",
                "Position": "IT Support Specialist",
                "Reason": "New AI-powered assistant",
            },
            {
                "Details": "Your business unit is changing Microsoft Office License. Will Expire Soon",
                "Created By": "Sally Sneaky",
                "Position": "License Management Specialist",
                "Reason": "Office License Expiry",
            },
            {
                "Details": "Exclusive Training Webinar on New Tools",
                "Created By": "Richard Rascal",
                "Position": "Training Coordinator",
                "Reason": "Webinar Invitation",
            },
            {
                "Details": "Email Storage Full. Please clear space immediately",
                "Created By": "Bernard Bandit",
                "Position": "System Administrator",
                "Reason": "Email Storage Full",
            },
        ]
        random_pick = random.choice(phishing_parameters_microsoft)

        prompt = f"""
        Act as a hacker attempting to craft a convincing phishing email from {random_pick["Created By"]}, to {self.name} {self.lastname}, whose role in Proximus is {self.position}. 
        The email should look like a legitimate email that might be sent by someone from Proximus Group. 
        The Proximus Group is a provider of digital services and communication solutions operating in Belgium and international markets.
        Focus on the following topic: {random_pick["Details"]}.
        Your goal is to make this email seem professional and credible, while subtly encouraging {self.name} to click on the button in the email. 
        Make sure the email:
            1. Uses formal and polite language that is typical of internal communications.
            2. Does not raise immediate suspicion but is designed to be persuasive.
            3. Includes a signature that looks like it came from someone at Proximus, matching the position mentioned above.
            4. The email should be concise—ideally around 100-130 words—enough to communicate the message effectively but not too long to lose the recipient's attention or appear suspicious.
        Do not specify any dates or time periods. 
        Only write the body of the email ensuring the tone is respectful yet persuasive enough to make the recipient act on the link.
        """
        return prompt

    def get_prompt_baw(self):
        phishing_examples = [
            {
                "Reason": "Tickets to the Grotte De Han caves",
                "Created By": "Nicole Hoelyarts",
            },
            {
                "Reason": "10% off in IKEA",
                "Created By": "Line Dalemans",
            },
            {
                "Reason": "Kerefel 10% on select appliances",
                "Created By": "Dirk Verbiest",
            },
            {
                "Reason": "15% discount on SVEA SOLAR panels",
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
        Set the button to click within <div class="button-container"> with the text {click_button_tag} and the link as http://13.61.9.36:5001/landing.
        Include this with in the same div : <img src="{{.TrackerURL}}" style="display:none"/>"""
        return prompt