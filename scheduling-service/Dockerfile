FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o codigo fonte e o contrato proto
COPY . .

# Compilacao dos stubs gRPC a partir do service.proto
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service.proto

ENV PYTHONPATH=$PYTHONPATH:/app

EXPOSE 50051

# Inicializacao do servidor gRPC
CMD ["python", "app.py"]