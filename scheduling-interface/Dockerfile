FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o main.py e os arquivos service_pb2 que você moveu para cá
COPY . .

# Expõe a porta que o FastAPI usa
EXPOSE 8000

# Comando para rodar a interface (importante usar 0.0.0.0 para o Docker)
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]