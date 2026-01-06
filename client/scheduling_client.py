import grpc
import service_pb2
import service_pb2_grpc

def run():
    # Conecta ao servidor gRPC
    with grpc.insecure_channel('scheduling:50051') as channel:
        stub = service_pb2_grpc.SchedulingServiceStub(channel)
        
        while True:
            print("\n" + "="*30)
            print("    SISTEMA DE AGENDAMENTO")
            print("="*30)
            print("1. AGENDAR")
            print("2. VERIFICAR STATUS")
            print("3. ATUALIZAR")
            print("0. SAIR")
            print("="*30)
            
            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                paciente = input("Nome do paciente: ")
                medico = input("Nome do médico: ")
                horario = input("Horário (ex: 10:00): ")
                
                response = stub.ScheduleAppointment(service_pb2.AppointmentRequest(
                    paciente=paciente, medico=medico, horario=horario
                ))
                print(f"\n=> {response.mensagem}")
                print(f"=> Status: {response.status}")

            elif opcao == '2':
                id_c = input("Digite o ID da consulta para VERIFICAR STATUS: ")
                print(f"\n=> Consultando status do ID {id_c} no servidor...")
                # Lógica gRPC de consulta aqui

            elif opcao == '3':
                id_c = input("Digite o ID da consulta para ATUALIZAR: ")
                try:
                    response = stub.ConfirmAppointment(service_pb2.ConfirmRequest(id_consulta=int(id_c)))
                    print(f"\n=> {response.mensagem}")
                except ValueError:
                    print("❌ Erro: O ID deve ser um número inteiro.")

            elif opcao == '0':
                print("Saindo...")
                break
            else:
                print("❌ Opção inválida!")

if __name__ == '__main__':
    run()