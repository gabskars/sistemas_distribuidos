import pika
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="rabbitmq")
)
channel = connection.channel()
channel.queue_declare(queue="notifications")

def callback(ch, method, properties, body):
    print("🔔", json.loads(body))

channel.basic_consume(
    queue="notifications",
    on_message_callback=callback,
    auto_ack=True
)

print("📡 Aguardando notificações...")
channel.start_consuming()