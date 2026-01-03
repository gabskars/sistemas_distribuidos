from fastapi import FastAPI, HTTPException
import grpc
import os
import service_pb2
import service_pb2_grpc

app = FastAPI(title="Interface de Agendamento - Sistemas Distribuídos")

# Configuração do endereço do servidor gRPC
# No Docker, usamos o nome do serviço 'scheduling-service'
# No Windows (teste local), usamos 'localhost'
GRPC_SERVER = os.getenv("GRPC_SERVER_ADDRESS", "scheduling-service:50051")

def get_stub():
    """Cria o canal de comunicação com o servidor gRPC."""
    channel = grpc.insecure_channel(GRPC_SERVER)
    return service_pb2_grpc.SchedulingServiceStub(channel)

# --- Endpoint REST para criar Agendamento ---
@app.post("/agendar")
async def agendar_consulta(paciente_id: str, medico_id: str, especialidade: str, data_hora: str):
    print(f"🌐 Interface: Recebido pedido de agendamento para {paciente_id}")
    
    try:
        stub = get_stub()
        # Monta a requisição gRPC baseada no seu service.proto
        request = service_pb2.AppointmentRequest(
            patient_id=paciente_id,
            doctor_id=medico_id,
            specialty=especialidade,
            date_time=data_hora
        )
        
        # Faz a chamada gRPC ao Coração do Sistema
        response = stub.CreateAppointment(request)
        
        # Se o gRPC retornar erro de regra de negócio (conflito de horário)
        if response.status == "ERRO":
            raise HTTPException(status_code=400, detail=response.message)
        
        # Retorno de sucesso formatado para o agendar.py
        return {
            "status": response.status, 
            "id_consulta": response.appointment_id, 
            "mensagem": response.message
        }
    except grpc.RpcError as e:
        print(f"❌ Erro gRPC: {e}")
        raise HTTPException(status_code=503, detail="Serviço de agendamento indisponível")

# --- Endpoint REST para consultar Status ---
@app.get("/status/{id_consulta}")
async def consultar_status(id_consulta: str):
    print(f"🌐 Interface: Consultando status do ID {id_consulta}")
    
    try:
        stub = get_stub()
        request = service_pb2.StatusRequest(appointment_id=id_consulta)
        response = stub.GetAppointmentStatus(request)
        
        if response.status == "Não encontrada":
             raise HTTPException(status_code=404, detail="Consulta não localizada no banco de dados.")
             
        return {
            "id_consulta": id_consulta, 
            "status": response.status
        }
    except grpc.RpcError as e:
        print(f"❌ Erro gRPC: {e}")
        raise HTTPException(status_code=503, detail="Não foi possível falar com o servidor gRPC.")

# --- Endpoint REST para atualizar Status (Opcional para integração) ---
@app.put("/status/{id_consulta}")
async def atualizar_status(id_consulta: str, novo_status: str):
    try:
        stub = get_stub()
        request = service_pb2.UpdateStatusRequest(appointment_id=id_consulta, new_status=novo_status)
        response = stub.UpdateStatus(request)
        
        if response.status == "ERRO":
            raise HTTPException(status_code=400, detail=response.message)
            
        return {"id_consulta": id_consulta, "status": response.status, "mensagem": response.message}
    except grpc.RpcError:
        raise HTTPException(status_code=503, detail="Erro ao atualizar status via gRPC.")