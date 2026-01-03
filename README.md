# Módulo de Agendamento - Sistemas Distribuídos (UFC)

Este módulo é responsável pela gestão de agendamentos médicos, utilizando uma arquitetura distribuída que combina **REST** para comunicação com o cliente e **gRPC** para comunicação interna entre serviços.

## 🏗️ Arquitetura
O sistema é dividido em três partes principais:
1. **Lado Cliente (Scripts Python):** Interface de linha de comando para o usuário.
2. **Interface REST (FastAPI):** Atua como um API Gateway, recebendo requisições HTTP e traduzindo para chamadas gRPC.
3. **Serviço de Agendamento (gRPC):** O sistema onde reside a lógica de negócio e a persistência em banco de dados **SQLite**.

## 🛠️ Tecnologias Utilizadas
- **Python 3.13**
- **gRPC** (Comunicação de alto desempenho)
- **FastAPI** (Interface REST)
- **Docker & Docker Compose** (Containerização e Orquestração)
- **SQLite** (Persistência de dados)

## 🚀 Como Executar
Certifique-se de ter o Docker instalado e execute o comando abaixo na raiz do projeto:

```bash
docker-compose up --build