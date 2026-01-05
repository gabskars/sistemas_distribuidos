import pika
import json

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
    print(f"📥 Consumidor iniciado - Fila: {QUEUE_NAME}\n")
    
    # Callback para processar mensagens
    def callback(ch, method, properties, body):
        try:
            message = json.loads(body)
            print(f"🔔 Mensagem recebida: {message}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"❌ Erro ao processar mensagem: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
    
    # Consumir mensagens
    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback,
        auto_ack=False
    )
    
    print("⏳ Aguardando notificações...\n")
    channel.start_consuming()
    
except KeyboardInterrupt:
    print("\n🛑 Consumidor finalizado")
    if connection:
        connection.close()
except Exception as e:
    print(f"❌ Erro: {e}")
finally:
    if connection:
        connection.close()