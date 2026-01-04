Modulo de Agendamento - Sistemas Distribuidos UFC
Como rodar em outra maquina:

Clone o repositorio: git clone https://github.com/gabskars/sistemas_distribuidos.git

Entre na pasta: cd projeto-sd

Mude para a branch: git fetch origin && git checkout feature-agendamento-ismael

Como iniciar o sistema:

Na raiz do projeto, execute: docker-compose up --build

Roteiro de testes (Executar dentro da pasta client):

Criar agendamento: python agendar.py "Ismael" "Dr_Filipe" "Sistemas" "2026-01-10_10:00"

Testar conflito (mesmo medico e horario): python agendar.py "Teste" "Dr_Filipe" "Sistemas" "2026-01-10_10:00"

Consultar status: python status.py 1

Comandos de reset:

Para parar e limpar o ambiente: docker-compose down -v --remove-orphans