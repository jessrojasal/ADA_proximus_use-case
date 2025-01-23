FROM python:3.9-slim
WORKDIR /app
COPY . /app


# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    chromium \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libgdk-pixbuf2.0-0 \
    libgtk-3-0 \
    libgbm1 \
    libasound2

# Download ChromeDriver
RUN wget https://storage.googleapis.com/chrome-for-testing-public/132.0.6834.110/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    chmod +x chromedriver-linux64/chromedriver && \
    mv chromedriver-linux64/chromedriver /usr/bin/chromedriver


RUN pip install -r requirements.txt
RUN pip install selenium
ENV PYTHONUNBUFFERED=1
EXPOSE 5001
CMD ["python", "main.py"]

