import pika
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="rabbitmq")
)
channel = connection.channel()

channel.queue_declare(queue="tarefas", durable=True)

def callback(ch, method, properties, body):
    print(f"[CONSUMER] Processando: {body.decode()}")
    time.sleep(2)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)

channel.basic_consume(
    queue="tarefas",
    on_message_callback=callback
)

print("[CONSUMER] Aguardando mensagens...")
channel.start_consuming()