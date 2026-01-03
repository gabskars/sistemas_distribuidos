FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia os arquivos do projeto e o contrato proto
COPY . .

# Compila os arquivos gRPC (stubs) a partir do service.proto
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service.proto

# Garantia de que modulos gerados sejam encontrados
ENV PYTHONPATH=$PYTHONPATH:/app

# Porta de comunicacao da API REST
EXPOSE 8000

# Inicializacao do servidor FastAPI com Uvicorn
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]