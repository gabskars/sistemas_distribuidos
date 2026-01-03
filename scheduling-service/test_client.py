import grpc
import service_pb2
import service_pb2_grpc

def run_test():
    # Conecta ao seu servidor gRPC
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.SchedulingServiceStub(channel)

        print("--- TESTE 1: Criando agendamento novo ---")
        request = service_pb2.AppointmentRequest(
            patient_id="User_01", 
            doctor_id="Dr_Filipe",
            specialty="Computacao", 
            date_time="2026-01-10 14:00"
        )
        response = stub.CreateAppointment(request)
        print(f"Resultado: {response.status} - {response.message}")

        print("\n--- TESTE 2: Tentando o MESMO médico e horário (Conflito) ---")
        # O sistema deve bloquear este segundo pedido automaticamente
        response2 = stub.CreateAppointment(request) 
        print(f"Resultado: {response2.status} - {response2.message}")

if __name__ == '__main__':
    run_test()