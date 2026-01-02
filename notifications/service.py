import time


def start_notification_service():
    """
    Serviço de Notificações
    Publica notificações via RabbitMQ.
    Atua como Publisher.
    """
    print("[NotificationService] Serviço de Notificações iniciado.")

    while True:
        time.sleep(1)