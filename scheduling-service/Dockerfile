# Usa uma imagem leve do Python 3.13
FROM python:3.13-slim

# Define a pasta oficial do projeto dentro do container
WORKDIR /app

# Copia a lista de dependências e instala
# Usamos o cache do Docker para agilizar builds futuros
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da pasta scheduling-service para dentro do container
COPY . .

# GERA OS ARQUIVOS gRPC: Esta linha sincroniza a versão do gencode com o runtime
# Ela transforma o service.proto nos arquivos .py que o app.py importa
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service.proto

# GARANTIA: Adiciona a pasta /app ao caminho de busca do Python
# Isso evita o erro de "ModuleNotFound" mesmo se o Docker mudar a estrutura interna
ENV PYTHONPATH=$PYTHONPATH:/app

# Informa que o container usará a porta 50051 para o gRPC
EXPOSE 50051

# Comando definitivo para ligar o servidor
CMD ["python", "app.py"]