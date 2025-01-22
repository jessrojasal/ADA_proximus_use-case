# Installation and Usage

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

1. Make sure all dependencies are installed in a virtual environment:
```bash
pip install -r requirements.txt
```

2. Start the Flask server:
```python
python ./main.py
```

3. Start the Gophish server:
In the `./gophish_engine` directory execute
```bash
./gophish
```

4. To go to the user interface, go to the flask endoint printed in the terminal. To go to the gophish admin page go to the address printed in the terminal where the `gophish` command was executed.
