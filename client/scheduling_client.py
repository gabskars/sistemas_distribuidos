import grpc
import service_pb2
import service_pb2_grpc
import sys

def run():
    try:
        # Conexao com o servidor definido no docker-compose
        with grpc.insecure_channel('scheduling:50051') as channel:
            stub = service_pb2_grpc.SchedulingServiceStub(channel)
            
            while True:
                print("\n" + "="*45)
                print("      SISTEMA DE AGENDAMENTO (GERENCIADOR)")
                print("="*45)
                print("  1. REALIZAR AGENDAMENTO")
                print("  2. CONSULTAR STATUS")
                print("  3. ATUALIZAR STATUS (COMPATIBILIDADE)")
                print("  0. SAIR")
                print("="*45)
                
                opcao = input("Escolha uma opcao: ")

                if opcao == '1':
                    print("\n--- Formulario de Agendamento ---")
                    paciente = input("Nome do Paciente: ")
                    medico = input("Nome do Medico: ")
                    especialidade = input("Especialidade Medica: ")
                    # Formato exigido: ano-mes-dia hora:minutos
                    horario = input("Data/Hora (AAAA-MM-DD HH:MM): ")
                    
                    # Chamada CreateAppointment (Compativel com seu service.proto)
                    response = stub.CreateAppointment(service_pb2.AppointmentRequest(
                        paciente=paciente, 
                        medico=medico, 
                        especialidade=especialidade, 
                        horario=horario
                    ))
                    
                    print(f"\n=> RESPOSTA DO SERVIDOR:")
                    print(f"   ID Gerado: {response.id_consulta}")
                    print(f"   Status da Operacao: {'SUCESSO' if response.sucesso else 'FALHA'}")
                    print(f"   Mensagem: {response.mensagem}")

                elif opcao == '2':
                    try:
                        id_c = int(input("\nDigite o ID para consulta: "))
                        response = stub.GetStatus(service_pb2.StatusRequest(id_consulta=id_c))
                        print(f"\n🔍 STATUS ATUAL: {response.status}")
                    except ValueError:
                        print("\n[!] Erro: O ID precisa ser numerico.")

                elif opcao == '3':
                    try:
                        id_c = int(input("\nID da consulta para atualizar: "))
                        print("Opcoes: Pendente, Confirmado, Cancelado")
                        novo_status = input("Novo Status: ")
                        
                        response = stub.UpdateStatus(service_pb2.UpdateRequest(
                            id_consulta=id_c, 
                            novo_status=novo_status
                        ))
                        
                        if response.sucesso:
                            print(f"\n✅ ATUALIZADO: {response.mensagem}")
                        else:
                            print(f"\n❌ ERRO: {response.mensagem}")
                    except ValueError:
                        print("\n[!] Erro: O ID precisa ser numerico.")

                elif opcao == '0':
                    print("\nDesconectando...")
                    break
                else:
                    print("\n[!] Opcao invalida.")

    except grpc.RpcError as e:
        print(f"\n[!] Erro de comunicacao gRPC: {e.details()}")
    except Exception as e:
        print(f"\n[!] Erro critico: {e}")

if __name__ == '__main__':
    run()