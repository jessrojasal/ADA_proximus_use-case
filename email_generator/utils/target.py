import google.generativeai as genai
from ..utils.prompt import Prompt
from time import sleep

class PhishingTarget:
    def __init__(self, data, model):
        self.data = data
        self.model = model

    def generate_email(self, topic):
        """
        Generates an email for every given user details
        """
        print(f"Generating email for {self.data['name']} {self.data['last_name']}")
        user_prompt = Prompt(
            self.model, self.data["name"], self.data["last_name"], self.data["position"]
        )
        click_button_tag = "Click here"
        if (topic == "Benefits At Work"):
            prompt = user_prompt.get_prompt_baw()
            click_button_tag = "Claim offer"
        elif (topic == "Microsoft"):
            prompt = user_prompt.get_prompt_microsoft()
            click_button_tag = "Activate now"
        elif (topic == "LinkedIn"):
            if self.data["Licenses & certifications"] != '':
                prompt = user_prompt.linkedin_cert(self.data["Licenses & certifications"])
                click_button_tag = "Renew now"
            else:
                prompt = user_prompt.get_prompt_microsoft()
            
        body = self.model.generate_content(prompt)
        sleep(3)
        #print(body.text)
        html_prompt = user_prompt.generate_html_tags(body.text, click_button_tag)
        sleep(3)
        #print(html_prompt)
        html_body = self.model.generate_content(html_prompt)

        subject = self.model.generate_content(
            "Write me the subject of this email:\n" + body.text
        )
        header,footer = self.return_header_footer()
        html_content = f"{header}{html_body.text}{footer}"
        self.data["body"] = html_content
        self.data["subject"] = subject.text

    def return_header_footer(self):
        header = """
            <!DOCTYPE html>
            <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Proximus notifications</title>
            <style>
                body {
                    font-family: Verdana;
                    margin: 0;
                    padding: 0;
                    background-color: #f5f5f5;
                }
                .email-container {
                    max-width: 800px;
                    margin: 50px auto;
                    background-color: #ffffff;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    overflow: hidden;
                }
                .header {
                    display: flex;
                    align-items: center;
                    background-color: #4b0082;
                    padding: 25px;
                }
                .header h1, 
                .header h2 {
                    margin: 0;
                } 
                .header h1 {
                    font-size: 18px;
                    margin-right: 5px;
                    color: #ffffff
                }
                .header h2 {
                    font-size: 12px;
                    margin: 0px;
                    margin-bottom: -3px;
                    color: #ffffff;
                    font-weight: bold;
                }
                .header img {
                    max-width: 300px;
                }
                .content {
                    padding: 40px;
                }
                .content h3 {
                    font-size: 18px;
                    margin: 0 0 15px;
                }

                .content p {
                    font-size: 14px;
                    color: #555;
                    margin: 0 0 10px;
                    line-height: 1.7;
                }
                .button-container {
                    text-align: center;
                    margin: 20px 0;
                }
                .button-container a {
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #f5f5f5;
                    color: #000;
                    text-decoration: none;
                    border-radius: 3px;
                    border: 1px solid #ddd;
                    font-size: 14px;
                }
                .footer {
                    padding: 20px;
                    background-color: #4b0082;
                    color: #ffffff;
                    font-size: 12px;
                    text-align: center;
                }
                .footer a {
                    color: #ffffff;
                    text-decoration: none;
                    margin: 0 5px;
                }
                .footer a:hover {
                    text-decoration: underline;
                }
                .footer .footer-logo {
                    align-items: center;
                    justify-content: center;
                    margin-bottom: 10px;
                }
                .footer .footer-logo img {
                    max-width: 90px;
                    margin-right: 20px;
                }
            </style>
        </head>
        <body>

        <div class="email-container">
            <!-- Header Section -->
            <div class="header">
                <h1>Proximus Group | </h1>
                <h2>Boldly building a connected world that people trust so society blooms</h2>
            </div>
        <div class="content">
        """.strip()

        footer = """
        </div>
                <div class="footer">
                    <p>All rights reserved. © Proximus 2025.</p>
                    <a href=".">Unsubscribe</a> | <a href=".">Learn</a> | <a href=".">Help Center</a>
                    <p>Boulevard du Roi Albert 2, 27 B-1030 Brussels</p>
                    </p>
                </div>
            </div>

            </body>
        </html>
        """.strip()

        return (header,footer)