# Usa a imagem Python 3.13-slim para manter o container leve
FROM python:3.13-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia e instala as dependências (FastAPI, Uvicorn, gRPC, etc)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da interface e o arquivo service.proto para dentro do container
COPY . .

# GERA OS ARQUIVOS gRPC NA INTERFACE: 
# Isso permite que a API REST saiba como conversar com o servidor gRPC
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service.proto

# GARANTIA: Define o caminho de busca do Python para evitar erros de importação
ENV PYTHONPATH=$PYTHONPATH:/app

# Expõe a porta 8000, que é por onde o agendar.py vai se conectar
EXPOSE 8000

# Inicia o servidor Uvicorn para rodar a API FastAPI
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]