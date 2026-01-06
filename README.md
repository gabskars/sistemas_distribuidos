
       PROJETO DE SISTEMAS DISTRIBUIDOS - AGENDAMENTO

Este sistema utiliza gRPC para comunicacao entre o cliente 
e o servidor de agendamento, com integracao ao RabbitMQ.

COMO EXECUTAR:

1. Na pasta raiz, rode o comando:
   docker-compose up --build -d

2. Aguarde os containers ficarem com status "Up".

COMO TESTAR O MENU:

1. Use o comando abaixo para entrar no terminal interativo:
   docker exec -it sistemas_distribuidos-client-1 python3 scheduling_client.py

FUNCIONALIDADES DO MENU:

- OPCAO 1: Realiza o agendamento completo. 
  OBS: Use a data no formato AAAA-MM-DD HH:MM para evitar erros.
  
- OPCAO 2: Consulta se a consulta existe e qual o status.

- OPCAO 3: Funcao de compatibilidade para forcar a atualizacao
  de um status no banco de dados.

RESOLUCAO DE PROBLEMAS (RESET):

Caso o container nao suba ou de erro de arquivo faltando:
docker-compose down -v
docker-compose up --build -d


============================================================
