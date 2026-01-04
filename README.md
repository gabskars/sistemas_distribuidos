🏥 Módulo de Agendamento - Sistemas Distribuídos (UFC)
Este repositório contém a minha parte da 3ª AP: o sistema de agendamento médico. A ideia aqui foi separar a lógica em microserviços pra garantir que o sistema seja escalável e não dê gargalo.

🏗️ Como o sistema funciona:
Interface (Porta 8000): É uma API REST em FastAPI que serve como a porta de entrada.

Service (Porta 50051): É o servidor gRPC onde fica o "grosso" da lógica e a conexão com o banco.

Banco de Dados: Usei SQLite pela praticidade de não precisar subir um servidor de banco pesado.

📥 Como rodar na sua máquina 

Bash

# Entra na branch do agendamento
git fetch origin
git checkout feature-agendamento-ismael
git pull origin feature-agendamento-ismael

# Sobe tudo pelo Docker (Isso já compila o gRPC e instala as libs)
docker-compose up --build


🧪 Roteiro de Testes (Siga esta ordem)
Abra um terminal dentro da pasta client/ e rode os comandos abaixo.

Agendar uma consulta (Caminho Feliz): 
python agendar.py "Ismael" "Dr_Filipe" "Sistemas" "2026-01-10_10:00" 
Dica: Se for o primeiro teste, o ID gerado vai ser o 1.

Testar erro de conflito (Mesmo médico e horário): 
python agendar.py "Teste" "Dr_Filipe" "Sistemas" "2026-01-10_10:00" 
O gRPC deve bloquear e retornar que o horário está ocupado.



Ver o status da consulta: 
python status.py 1

Confirmar a consulta (Atualizar status): 
python atualizar.py 1 "Confirmada"



🧹 Comandos Úteis e Reset

Para parar tudo: 
docker-compose down

Para limpar volumes e redes: 
docker-compose down -v --remove-orphans


📂 O que tem em cada pasta:
/client: Scripts para você testar no terminal.

/scheduling-interface: Onde está a API REST.

/scheduling-service: Onde está o servidor gRPC e o banco.