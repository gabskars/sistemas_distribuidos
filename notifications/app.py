import pika
import json
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="rabbitmq")
)
channel = connection.channel()
channel.queue_declare(queue="notifications")

while True:
    msg = {
        "mensagem": "Consulta atualizada",
        "status": "CONFIRMADA"
    }

    channel.basic_publish(
        exchange="",
        routing_key="notifications",
        body=json.dumps(msg)
    )

    print("📨 Notificação enviada")
    time.sleep(10)