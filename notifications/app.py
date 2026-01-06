import pika
import json
import time
import sys

# Configurações
RABBITMQ_HOST = "rabbitmq"
QUEUE_NAME = "notifications"

# 1. IMPORTANTE: Inicializa como None para evitar o NameError
connection = None

try:
    print(f"⏳ Aguardando RabbitMQ em {RABBITMQ_HOST}...")
    
    # 2. Tenta conectar (com um pequeno retry manual para estabilidade no Docker)
    for i in range(5):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST)
            )
            break 
        except pika.exceptions.AMQPConnectionError:
            print(f"  (Tentativa {i+1}/5) RabbitMQ ainda não está pronto, aguardando...")
            time.sleep(5)
    
    if not connection:
        print("❌ Não foi possível conectar ao RabbitMQ após várias tentativas.")
        sys.exit(1)

    channel = connection.channel()
    
    # Declarar a fila (durable=True para não perder mensagens se o broker cair)
    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True,
        auto_delete=False
    )
    
    print(f"✅ Conectado ao RabbitMQ")
    print(f"📤 Publicador iniciado - Fila: {QUEUE_NAME}\n")
    
    # Loop de publicação (Simulação de envio de notificações)
    while True:
        msg = {
            "mensagem": "Consulta atualizada",
            "status": "CONFIRMADA",
            "timestamp": time.time()
        }
        
        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=json.dumps(msg),
            properties=pika.BasicProperties(
                delivery_mode=2  # Mensagem persistente
            )
        )
        
        print(f"📨 Notificação enviada: {msg}")
        time.sleep(10)
        
except Exception as e:
    print(f"❌ Erro crítico no Publicador: {e}")

finally:
    # 3. Fechamento seguro: verifica se a variável existe e se está aberta
    if connection and not connection.is_closed:
        connection.close()
        print("🔌 Conexão com RabbitMQ fechada.")