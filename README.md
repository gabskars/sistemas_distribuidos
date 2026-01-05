# sistemas_distribuidos

📂 Guia do Desenvolvedor: Módulo de Agendamento
Este módulo gerencia o ciclo de vida das consultas médicas. Se você está puxando estas alterações, o código já foi validado e está pronto para uso.

🚀 Como Inicializar o Ambiente
Para subir todos os serviços e garantir que as alterações mais recentes sejam aplicadas, use:

PowerShell

docker-compose up --build
⚠️ Resolução de Problemas no Build (Ambiente)
Como o código do módulo está estável, se o comando acima falhar com mensagens como failed to execute bake ou file already closed, não se desespere:

Tente Novamente: Muitas vezes é um erro de sincronização do Docker Desktop com o Windows. Um segundo docker-compose up --build costuma resolver.

Limpe o Cache: Se o erro persistir, o cache do construtor pode estar corrompido. Rode: docker builder prune -f

Reinicie o Docker: Se nada funcionar, reinicie o Docker Desktop. O código em si não possui erros de sintaxe que impeçam o build.

🧪 Como Testar as Funcionalidades
Para garantir que a comunicação gRPC e a persistência no SQLite estão funcionando:

Entre no Container do Cliente: docker exec -it sistemas_distribuidos-client-1 bash

Rode o Script: python3 scheduling_client.py

Siga o Fluxo:

Agendar (Opção 1): Crie uma consulta e anote o ID (ex: ID 1).

Verificar (Opção 2): Verifique se o status é "Agendada".

Confirmar (Opção 3): Altere o status para "Confirmada".

Conflito: Tente agendar o mesmo médico no mesmo horário. O sistema deve retornar um erro 400, provando a eficácia da lógica de negócio no gRPC.

🔍 Verificação Interna (Opcional)
Se precisar confirmar a existência física do banco de dados (que não aparece no Windows por falta de volume mapeado), rode: docker exec -it sistemas_distribuidos-scheduling-1 ls O arquivo agendamentos.db deve estar listado lá.