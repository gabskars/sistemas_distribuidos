"""
Sistema de Gerenciamento de Consultas Médicas
Disciplina: Sistemas Distribuídos

Arquivo principal responsável por inicializar
todos os serviços do Lado Servidor.
"""

import threading
import time


# Importação das interfaces dos serviços
from users.interface import start_user_service
from scheduling.interface import start_scheduling_service
from validation.interface import start_validation_service
from notifications.service import start_notification_service


def start_all_services():
    """
    Inicializa todos os serviços do sistema em paralelo.
    Cada serviço roda em sua própria thread.
    """

    services = [
        threading.Thread(
            target=start_user_service,
            name="UserService"
        ),
        threading.Thread(
            target=start_scheduling_service,
            name="SchedulingService"
        ),
        threading.Thread(
            target=start_validation_service,
            name="ValidationService"
        ),
        threading.Thread(
            target=start_notification_service,
            name="NotificationService"
        )
    ]

    for service in services:
        service.start()
        print(f"[MAIN] {service.name} iniciado com sucesso.")

    # Mantém o processo principal ativo
    for service in services:
        service.join()


if __name__ == "__main__":
    print("=" * 50)
    print("  SISTEMA DE GERENCIAMENTO DE CONSULTAS")
    print("  Inicializando serviços do servidor...")
    print("=" * 50)

    try:
        start_all_services()
    except KeyboardInterrupt:
        print("\n[MAIN] Encerrando o sistema...")
        time.sleep(1)
        print("[MAIN] Sistema finalizado.")