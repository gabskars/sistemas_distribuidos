def start_notification_service():
    """
    Serviço de Notificações
    Publica notificações via RabbitMQ.
    Atua como Publisher.
    """
    print("[NotificationService] Serviço de Notificações iniciado.")
    import pika
    import time
    import json
    from datetime import datetime

    RABBIT_HOST = "rabbitmq"
    QUEUE_NAME = "notifications"

    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBIT_HOST)
            )

            channel = connection.channel()
            channel.queue_declare(queue=QUEUE_NAME, durable=True)

            counter = 1
            print("[NotificationService] Conectado ao RabbitMQ, publicando notificações")

            while True:
                payload = {
                    "id": counter,
                    "message": f"Notificação {counter}",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }

                body = json.dumps(payload).encode()

                channel.basic_publish(
                    exchange="",
                    routing_key=QUEUE_NAME,
                    body=body,
                    properties=pika.BasicProperties(delivery_mode=2)
                )

                print(f"[NotificationService] Enviado: {payload}")
                counter += 1
                time.sleep(5)

        except Exception as e:
            print(f"[NotificationService] Erro na conexão/publicação: {e}")
            try:
                connection.close()
            except Exception:
                pass
            print("[NotificationService] Tentando reconectar em 5s...")
            time.sleep(5)