import grpc
from concurrent import futures
import sqlite3
import service_pb2
import service_pb2_grpc

# Esta classe gerencia a lógica do Coração do Sistema [cite: 18]
class SchedulingService(service_pb2_grpc.SchedulingServiceServicer):

    def CreateAppointment(self, request, context):
        print(f"Recebida tentativa de agendamento: Médico {request.doctor_id} em {request.date_time}")
        
        # Conexão com o Banco de Dados para persistir informações [cite: 16]
        conn = sqlite3.connect('agendamentos.db')
        cursor = conn.cursor()

        # REGRA DE NEGÓCIO: Evitar conflitos de horários e sobreposições 
        # Verificamos se já existe este médico ocupado neste mesmo horário
        cursor.execute('''
            SELECT id FROM consultas 
            WHERE medico_id = ? AND data_hora = ?
        ''', (request.doctor_id, request.date_time))
        
        conflito = cursor.fetchone()

        if conflito:
            conn.close()
            print(f"ALERTA: Conflito detectado para o médico {request.doctor_id}!")
            return service_pb2.AppointmentResponse(
                appointment_id="",
                status="ERRO",
                message="Este médico já possui uma consulta agendada para este horário."
            )

        # Se não houver conflito, o sistema permite o registro [cite: 53]
        cursor.execute('''
            INSERT INTO consultas (paciente_id, medico_id, especialidade, data_hora, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (request.patient_id, request.doctor_id, request.specialty, request.date_time, "Agendada"))
        
        appointment_id = str(cursor.lastrowid)
        conn.commit()
        conn.close()

        print(f"Sucesso: Consulta {appointment_id} registrada como 'Agendada'.")
        return service_pb2.AppointmentResponse(
            appointment_id=appointment_id,
            status="Agendada",
            message="Consulta marcada com sucesso!"
        )

    # Permite o acompanhamento da situação das consultas [cite: 56, 57]
    def GetAppointmentStatus(self, request, context):
        conn = sqlite3.connect('agendamentos.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT status FROM consultas WHERE id = ?', (request.appointment_id,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            return service_pb2.StatusResponse(
                appointment_id=request.appointment_id,
                status=resultado[0]
            )
        else:
            return service_pb2.StatusResponse(
                appointment_id=request.appointment_id,
                status="Não encontrada"
            )

# Configuração do Servidor gRPC [cite: 11, 23]
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_SchedulingServiceServicer_to_server(SchedulingService(), server)
    server.add_insecure_port('[::]:50051')
    print("Servidor de Agendamento (gRPC) rodando na porta 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()