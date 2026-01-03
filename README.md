🏥 Sistema Distribuído de Agendamento Médico
Este projeto foi desenvolvido para a disciplina de Sistemas Distribuídos (UFC). O sistema gerencia agendamentos médicos através de uma arquitetura de microserviços, utilizando REST para interface externa e gRPC para comunicação interna.

📥 Como Acessar este Módulo


Clone o repositório (caso ainda não tenha):

Bash

git clone [https://github.com/gabskars/sistemas_distribuidos.git]
cd projeto-sd
Baixe as branches remotas e acesse a minha branch:

Bash

git fetch origin
git checkout feature-agendamento-ismael
Garanta que está na versão mais recente:

Bash

git pull origin feature-agendamento-ismael
🚀 Como Executar o Projeto
Certifique-se de que o Docker Desktop está rodando. Na raiz do projeto, execute:

Bash

docker-compose up --build
Isso vai subir automaticamente o Servidor gRPC (Porta 50051) e a Interface REST (Porta 8000).

🧪 Guia de Testes (Passo a Passo)
Abra um novo terminal na pasta client/ para validar as funcionalidades:

1. Criar um Agendamento
Bash

python agendar.py "Ismael" "Dr_Filipe" "Sistemas" "2026-01-10_10:00"
Esperado: Mensagem de sucesso e geração do ID 1.

2. Validar Conflito de Horário
Bash

python agendar.py "Outro_Paciente" "Dr_Filipe" "Sistemas" "2026-01-10_10:00"
Esperado: Erro de horário ocupado (prova a lógica do gRPC).

3. Consultar Status
Bash

python status.py 1
4. Atualizar o Status
Bash

python atualizar.py 1 "Confirmada"
🧹 Comandos de Manutenção
Parar o sistema:

Bash

docker-compose down
Reset Total (Limpar banco e volumes):

Bash

docker-compose down -v --remove-orphans
Nota: Para resetar o banco SQLite, apague o arquivo agendamentos.db na pasta scheduling-service antes de subir o Docker.

📁 Estrutura
/client: Scripts CLI (agendar, status, atualizar).

/scheduling-interface: Gateway REST (FastAPI).

/scheduling-service: Servidor gRPC e SQLite.