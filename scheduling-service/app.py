import grpc
from concurrent import futures
import sqlite3
import service_pb2
import service_pb2_grpc
from database import init_db

# Implementação do Serviço gRPC
class SchedulingService(service_pb2_grpc.SchedulingServiceServicer):

    # Função 1: Criar Agendamento
    def CreateAppointment(self, request, context):
        print(f"📥 gRPC: Tentativa de agendamento para Médico {request.doctor_id}")
        conn = sqlite3.connect('agendamentos.db')
        cursor = conn.cursor()
        try:
            # Verifica conflito de horário
            cursor.execute('SELECT id FROM consultas WHERE medico_id = ? AND data_hora = ?', 
                           (request.doctor_id, request.date_time))
            if cursor.fetchone():
                return service_pb2.AppointmentResponse(appointment_id="", status="ERRO", message="Horário ocupado.")

            # Insere no banco
            cursor.execute('INSERT INTO consultas (paciente_id, medico_id, especialidade, data_hora, status) VALUES (?, ?, ?, ?, ?)',
                           (request.patient_id, request.doctor_id, request.specialty, request.date_time, "Agendada"))
            app_id = str(cursor.lastrowid)
            conn.commit()
            return service_pb2.AppointmentResponse(appointment_id=app_id, status="Agendada", message="Sucesso!")
        finally:
            conn.close()

    # Função 2: Consultar Status
    def GetAppointmentStatus(self, request, context):
        conn = sqlite3.connect('agendamentos.db')
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT status FROM consultas WHERE id = ?', (request.appointment_id,))
            res = cursor.fetchone()
            status = res[0] if res else "Não encontrada"
            return service_pb2.StatusResponse(appointment_id=request.appointment_id, status=status)
        finally:
            conn.close()

    # Função 3: ATUALIZAR STATUS (Nova, para bater com o .proto)
    def UpdateStatus(self, request, context):
        print(f"🔄 gRPC: Atualizando Consulta {request.appointment_id} para {request.new_status}")
        conn = sqlite3.connect('agendamentos.db')
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE consultas SET status = ? WHERE id = ?', 
                           (request.new_status, request.appointment_id))
            conn.commit()
            if cursor.rowcount > 0:
                return service_pb2.AppointmentResponse(appointment_id=request.appointment_id, status=request.new_status, message="Status atualizado.")
            else:
                return service_pb2.AppointmentResponse(appointment_id=request.appointment_id, status="ERRO", message="Consulta não encontrada.")
        finally:
            conn.close()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_SchedulingServiceServicer_to_server(SchedulingService(), server)
    server.add_insecure_port('[::]:50051')
    print("🚀 SERVIDOR gRPC ATIVO na porta 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    init_db()
    serve()