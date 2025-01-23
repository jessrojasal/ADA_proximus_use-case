FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN pip install selenium
ENV PYTHONUNBUFFERED=1
EXPOSE 5001
CMD ["python", "main.py"]

