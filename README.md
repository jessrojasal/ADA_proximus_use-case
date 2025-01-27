# Introduction

This is the first company use case of the Becode AI/data-science training from the Bouman-8 group. It aims to create a program to launch fully automated phishing campaings with AI-generated emails. The projects lasted two weeks and was made by
groups of 6-7 people. The group that contributed this repo consisted of 6 people of wich:
- 4 following the data analyst track:
  - Jessica (https://github.com/jessrojasal)
  - Dhanya (https://github.com/dha-code)
  - Mohammed (https://github.com/Mohammedhussingh)
  - Andrii (https://github.com/FomAndrii)
- 2 following the data engineer track:
  - Imad (https://github.com/7icee)
  - Maxim (https://github.com/MaximSchuermans)

# Installation and Usage

**Note**: Several environment variables and credentials are read in `config/settings.py` and `scraper/linkedin_credentials.json`. The program will not function as intended if these are not defined in a `.env` file.

## Install using Docker

1. Fetch the gophish image
```
docker pull gophish/gophish
```
2. Build the flask app cotainer:
```
docker build -t flask-app .
```
3. Run the gophish and flask containers:
```
docker run -d -p 5001:5001 flask-app
docker run -d -p 3333:3333 gophish/gophish
```

## Install manually

1. Make sure all dependencies are installed in a virtual environment (**seperatly** install selenium with pip):
```bash
pip install -r requirements.txt
pip install selenium
```

2. Download the `gophish` binary in the `gophish_engine` directory (see https://github.com/gophish/user-guide/blob/master/installation.md)

3. Start the Gophish server:
In the `./gophish_engine` directory execute
```bash
./gophish
```

4. Start the Flask server:
```python
python ./main.py
```

5. To go to the user interface, go to the flask endoint printed in the terminal. To go to the gophish admin page go to the address printed in the terminal where the `gophish` command was executed.

## Usage
The project has been divided into five main parts: a dashboard `app`, a scraper `scraper`, an email generator `email_generator`, a gophish setup `gophish_engine`, and a powerBI program. The main entrypoint is the
dashboard that can be found at the flask app URL found in the logs after executing `python main.py`. A file can be uploaded to this dashboard wich will trigger the main loop of reading the file, scraping information, and generating/sending emails.

# Presentation
A presentation was given on 24/01/2025 at the Becode campus in Brussels. This presentation contains a technical summary of the project. The slides can be found in the `presentation.pdf` file.
