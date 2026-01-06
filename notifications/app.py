import pika
import json
import time
import sys

# Configurações
RABBITMQ_HOST = "rabbitmq"
QUEUE_NAME = "notifications"

# Inicializa como None para evitar o NameError
connection = None

try:
    print(f"⏳ Aguardando RabbitMQ em {RABBITMQ_HOST}...")
    
    # Tenta conectar (com retry manual para estabilidade no Docker)
    for i in range(15):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST, connection_attempts=3, retry_delay=2)
            )
            break 
        except pika.exceptions.AMQPConnectionError:
            print(f"  (Tentativa {i+1}/15) RabbitMQ ainda não está pronto, aguardando...")
            time.sleep(10)
    
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
    print(f"📥 Consumidor iniciado - Fila: {QUEUE_NAME}\n")
    
    # Callback para processar mensagens
    def callback(ch, method, properties, body):
        try:
            msg = json.loads(body)
            print(f"📨 Notificação recebida: {msg}")
            
            # Processar a notificação aqui
            # (enviar email, SMS, push notification, etc.)
            
            # Confirmar que a mensagem foi processada
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print(f"✅ Notificação processada com sucesso\n")
            
        except Exception as e:
            print(f"❌ Erro ao processar notificação: {e}")
            # Rejeitar a mensagem e recolocá-la na fila
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
    
    # Configurar o consumidor
    channel.basic_qos(prefetch_count=1)  # Processa uma mensagem por vez
    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback,
        auto_ack=False
    )
    
    print("🔄 Aguardando mensagens...")
    channel.start_consuming()
        
except Exception as e:
    print(f"❌ Erro crítico no Consumidor: {e}")

finally:
    # Fechamento seguro
    if connection and not connection.is_closed:
        connection.close()
        print("🔌 Conexão com RabbitMQ fechada.")