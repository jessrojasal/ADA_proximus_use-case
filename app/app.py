from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename

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

if __name__ == '__main__':
    app.run(debug=True)

