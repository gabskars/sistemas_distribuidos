import pika
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="rabbitmq")
)
channel = connection.channel()

channel.queue_declare(queue="tarefas", durable=True)

for i in range(1, 6):
    mensagem = f"Tarefa {i}"

    channel.basic_publish(
        exchange="",
        routing_key="tarefas",
        body=mensagem.encode(),
        properties=pika.BasicProperties(
            delivery_mode=2  # mensagem persistente
        )
    )

    print(f"[PRODUCER] Enviado: {mensagem}")
    time.sleep(1)

connection.close()