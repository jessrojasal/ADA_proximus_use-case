# Installation and Usage

## Install using Docker

**Note**: Several environment variables and credentials are defined in config and setting files. The program will not function as intended if these are not defined.

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
