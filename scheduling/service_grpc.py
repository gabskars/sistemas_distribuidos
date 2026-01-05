import grpc
from concurrent import futures
import service_pb2
import service_pb2_grpc
import sqlite3

class SchedulingService(service_pb2_grpc.SchedulingServiceServicer):
    def __init__(self):
        self.db = "agendamentos.db"
        with sqlite3.connect(self.db) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS agendamentos (id INTEGER PRIMARY KEY, paciente TEXT, medico TEXT, horario TEXT, status TEXT)")

    def CreateAppointment(self, request, context):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            # Verifica conflito
            cursor.execute("SELECT * FROM agendamentos WHERE medico=? AND horario=?", (request.medico, request.horario))
            if cursor.fetchone():
                return service_pb2.AppointmentResponse(id_consulta=-1, mensagem="Erro: Horario ocupado", sucesso=False)
            
            cursor.execute("INSERT INTO agendamentos (paciente, medico, horario, status) VALUES (?, ?, ?, ?)",
                           (request.paciente, request.medico, request.horario, "Agendada"))
            return service_pb2.AppointmentResponse(id_consulta=cursor.lastrowid, mensagem="Sucesso", sucesso=True)

    def GetStatus(self, request, context):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT status FROM agendamentos WHERE id=?", (request.id_consulta,))
            row = cursor.fetchone()
            return service_pb2.StatusResponse(status=row[0] if row else "Nao encontrado")

    def UpdateStatus(self, request, context):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE agendamentos SET status=? WHERE id=?", (request.novo_status, request.id_consulta))
            sucesso = cursor.rowcount > 0
            msg = "Status atualizado" if sucesso else "ID nao encontrado"
            return service_pb2.UpdateResponse(sucesso=sucesso, mensagem=msg)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_SchedulingServiceServicer_to_server(SchedulingService(), server)
    server.add_insecure_port('[::]:50051')
    print("Servidor gRPC rodando na porta 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()