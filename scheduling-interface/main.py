from fastapi import FastAPI, HTTPException
import grpc
import service_pb2
import service_pb2_grpc

app = FastAPI()

# Função auxiliar para falar com o seu servidor gRPC (app.py) [cite: 23]
def get_grpc_response(request_data):
    # Conecta ao serviço de agendamento via gRPC [cite: 23]
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.SchedulingServiceStub(channel)
        return stub.CreateAppointment(request_data)

# Endpoint REST para agendar [cite: 22, 53]
@app.post("/agendar")
async def agendar_consulta(paciente_id: str, medico_id: str, especialidade: str, data_hora: str):
    # Monta a requisição gRPC [cite: 23, 73]
    request = service_pb2.AppointmentRequest(
        patient_id=paciente_id,
        doctor_id=medico_id,
        specialty=especialidade,
        date_time=data_hora
    )
    
    response = get_grpc_response(request)
    
    # Se o gRPC retornar erro de conflito, avisamos o cliente [cite: 55]
    if response.status == "ERRO":
        raise HTTPException(status_code=400, detail=response.message)
    
    # IMPORTANTE: A chave aqui deve ser 'id_consulta' para o script cliente encontrar
    return {
        "status": response.status, 
        "id_consulta": response.appointment_id, 
        "mensagem": response.message
    }

# Endpoint REST para consultar status [cite: 56, 57]
@app.get("/status/{id_consulta}")
async def consultar_status(id_consulta: str):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.SchedulingServiceStub(channel)
        request = service_pb2.StatusRequest(appointment_id=id_consulta)
        response = stub.GetAppointmentStatus(request)
        
        if response.status == "Não encontrada":
             raise HTTPException(status_code=404, detail="Consulta não localizada")
             
        return {"id_consulta": id_consulta, "status": response.status}