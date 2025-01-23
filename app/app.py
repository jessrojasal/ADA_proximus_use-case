from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from gophish import Gophish
from scraper.scraper import scraper
from email_generator.email_generation import process_csv_and_generate_emails
from gophish_engine.main import create_campaigns

API_KEY = "de15a463fccdf2bcede8c18d31f1643c638c87932b3881efde9e5a795b06ad17"
BASE_URL = "https://13.61.9.36:3333/"  # Change port and URL as needed
api = Gophish(API_KEY, host=BASE_URL, verify=False)  # Set verify=True for SSL

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure upload folder
UPLOAD_FOLDER = 'data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    # Fetch active campaigns from GoPhish
    campaigns = api.campaigns.get()
    print('Lenght of campaign data: ', len(campaigns)) 
    # Create a list of dictionaries containing campaign data
    campaign_data = []
    for campaign in campaigns:
        campaign_data.append({
            'id': campaign.id,
            'name': campaign.name,
            'status': campaign.status,
            'created_date': campaign.created_date,
        })

    return render_template('dashboard.html', campaigns=campaign_data)

# API endpoint to fetch campaigns (optional, if needed for AJAX)
@app.route('/api/campaigns', methods=['GET'])
def get_campaigns():
    campaigns = api.campaigns.get()
    return jsonify([campaign.as_dict() for campaign in campaigns])

@app.route('/upload', methods=['POST'])
def upload_file():
    # Debug: Check if the form was submitted
    print("Received POST request")

    # Check if 'file' is in the request
    if 'file' not in request.files:
        flash("No file part in the request")
        print("Error: No file part in the request")
        return redirect(url_for('index'))

    file = request.files['file']

    # Check if a file was selected
    if file.filename == '':
        flash("No file selected")
        print("Error: No file selected")
        return redirect(url_for('index'))

    # Debug: Print the filename
    print(f"Filename received: {file.filename}")

    # Save the file
    filename = secure_filename(file.filename)  # Sanitize filename
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    print(f"Saving file to: {save_path}")  # Debug: Check save path

    file.save(save_path)  # Save file
    flash(f"File '{filename}' uploaded successfully!")
    print("File uploaded successfully")
    
    #scraper(input_csv="./data/targets.csv", output_csv="./data/scraped_targets.csv")
    process_csv_and_generate_emails(output_file='./data/output.csv', targets_file='./data/scraped_targets.csv', model_key='./email_generator/key.json')
    create_campaigns(input_file='./data/output.csv')

    return redirect(url_for('index'))
    

@app.route('/landing', methods=['GET'])
def get_landing():
    return render_template('landing_page.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

