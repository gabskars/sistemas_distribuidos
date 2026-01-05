import pika
import json
import time

# Configurações
RABBITMQ_HOST = "rabbitmq"
QUEUE_NAME = "notifications"

try:
    # Conectar ao RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    channel = connection.channel()
    
    # Declarar a fila (não apaga se já existir)
    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True,
        auto_delete=False
    )
    
    print(f"✅ Conectado ao RabbitMQ")
    print(f"📤 Publicador iniciado - Fila: {QUEUE_NAME}\n")
    
    # Loop de publicação
    while True:
        msg = {
            "mensagem": "Consulta atualizada",
            "status": "CONFIRMADA"
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
    print(f"❌ Erro: {e}")
finally:
    if connection:
        connection.close()