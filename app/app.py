from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename

from email_generator.email_generation import process_csv_and_generate_emails
from gophish_engine.main import create_campaigns

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure folder exists

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
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
        return redirect(url_for('index'))
    except Exception as e:
        flash(f"An error occurred: {str(e)}")
        print(f"Exception: {e}")
        return redirect(url_for('index'))
    
    output_file, targets_file = '../data/output.csv', '../data/targets.csv'
    print(f'A file has been uploaded, the main loop will execute. Make sure that the key.json targets.csv files arer present! Tragets will be read from {targets_file} Emails will be written to {filename}')
    model = initialize_genai('../key.json')
    process_csv_and_generate_emails(targets_file , model, output_file)
    create_campaigns(output_file)

@app.route('/landing', methods=['GET'])
def get_landing():
    return render_template('landing_page.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

