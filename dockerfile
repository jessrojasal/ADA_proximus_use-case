FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y \
    build-essential \
    libatlas-base-dev \
    gfortran \
    && apt-get clean
RUN pip install --no-cache-dir numpy
RUN pip install -r requirements.txt
RUN pip install selenium
EXPOSE 5001
CMD ["python", "main.py"]

