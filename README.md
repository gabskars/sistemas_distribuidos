Sistema Distribuído de Agendamento Médico
Este projeto foi desenvolvido para a 3ª AP da disciplina de Sistemas Distribuídos (UFC). O sistema utiliza uma arquitetura de microserviços para gerenciar consultas médicas, garantindo persistência, concorrência e tratamento de conflitos de horários.

Arquitetura do Sistema
O sistema é composto por três camadas principais:

Client (Python Scripts): Scripts que simulam a interação do usuário final com o sistema.

Scheduling Interface (REST API - FastAPI): Atua como o Gateway do sistema. Recebe requisições HTTP e as traduz para chamadas gRPC de alta performance.

Scheduling Service (gRPC Server): O núcleo do sistema. Implementa a lógica de negócio, verifica conflitos de horários e gerencia o banco de dados SQLite.

Fluxo de Comunicação
Usuário (Script) ➔ REST (Porta 8000) ➔ gRPC (Porta 50051) ➔ Banco de Dados (SQLite)

Tecnologias e Requisitos
Linguagem: Python 3.13

Comunicação Interna: gRPC (Protocol Buffers)

Comunicação Externa: REST API (FastAPI)

Containerização: Docker & Docker Compose

Banco de Dados: SQLite (Persistência Local)

Como Executar o Projeto
Certifique-se de que o Docker Desktop está em execução no seu computador.

Clone o repositório e acesse a branch:

Bash

git checkout feature-agendamento-ismael
Suba os containers (Build Automático): Na raiz do projeto, execute:

Bash

docker-compose up --build
Aguarde as mensagens 🚀 SERVIDOR gRPC ATIVO e Uvicorn running on http://0.0.0.0:8000 aparecerem nos logs.

Guia de Testes (Passo a Passo)
Com os containers rodando, abra um novo terminal e navegue até a pasta client/ para validar o sistema.

1. Criar um Agendamento (Caminho Feliz)
Bash

python agendar.py "SeuNome" "Dr_Filipe" "Sistemas" "2026-01-10_14:00"
Esperado: Mensagem de sucesso e geração de um ID da Consulta (ex: 1).

2. Validar Regra de Negócio (Teste de Conflito)
Tente agendar para o mesmo médico no mesmo horário:

Bash

python agendar.py "OutroPaciente" "Dr_Filipe" "Sistemas" "2026-01-10_14:00"
Esperado: O sistema deve retornar um erro informando que o médico já possui uma consulta agendada para este horário.

3. Consultar Status do Agendamento
Use o ID gerado no passo 1:

Bash

python status.py 1
Esperado: Retorno do status atual (ex: Agendada).

4. Teste de Persistência
Pare os containers com Ctrl + C.

Rode docker-compose up novamente (sem o build).

Consulte o status do ID 1 novamente. Os dados devem permanecer lá.

Organização dos Arquivos
/client: Scripts agendar.py e status.py.

/scheduling-interface: API REST (FastAPI) e Dockerfile da interface.

/scheduling-service: Servidor gRPC, service.proto, lógica de banco de dados e Dockerfile do serviço.

docker-compose.yml: Orquestração da rede e dos containers.