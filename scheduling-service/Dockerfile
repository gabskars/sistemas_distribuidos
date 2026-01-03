# Usa uma imagem leve do Python
FROM python:3.13-slim

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Copia as dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da pasta para o container
COPY . .

# Expõe a porta que o gRPC usa
EXPOSE 50051

# Comando para iniciar o servidor gRPC
CMD ["python", "app.py"]