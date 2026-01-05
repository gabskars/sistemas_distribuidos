<<<<<<< HEAD
FROM python:3.10-slim
WORKDIR /app
CMD ["python3"]
=======
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["python", "app.py"]
>>>>>>> 8023b494537855fb5709809a9416342d96c9219d
