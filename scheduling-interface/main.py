from fastapi import FastAPI, HTTPException
import grpc
import os
import service_pb2
import service_pb2_grpc

app = FastAPI(title="Interface de Agendamento - Sistemas Distribuídos")

# Define o alvo do gRPC: usa o nome do servico no Docker ou localhost para dev
GRPC_SERVER = os.getenv("GRPC_SERVER_ADDRESS", "scheduling-service:50051")

def get_stub():
    # Abre canal inseguro com o backend gRPC
    channel = grpc.insecure_channel(GRPC_SERVER)
    return service_pb2_grpc.SchedulingServiceStub(channel)

@app.post("/agendar")
async def agendar_consulta(paciente_id: str, medico_id: str, especialidade: str, data_hora: str):
    print(f"🌐 Interface: Recebido pedido de agendamento para {paciente_id}")
    
    try:
        stub = get_stub()
        # Mapeia os parametros REST para a mensagem do Protobuf
        request = service_pb2.AppointmentRequest(
            patient_id=paciente_id,
            doctor_id=medico_id,
            specialty=especialidade,
            date_time=data_hora
        )
        
        response = stub.CreateAppointment(request)
        
        # Valida erro de negocio retornado pelo servico (ex: conflito de agenda)
        if response.status == "ERRO":
            raise HTTPException(status_code=400, detail=response.message)
        
        return {
            "status": response.status, 
            "id_consulta": response.appointment_id, 
            "mensagem": response.message
        }
    except grpc.RpcError as e:
        print(f"❌ Erro gRPC: {e}")
        raise HTTPException(status_code=503, detail="Servico gRPC offline ou inacessivel")

@app.get("/status/{id_consulta}")
async def consultar_status(id_consulta: str):
    print(f"🌐 Interface: Consultando status do ID {id_consulta}")
    
    try:
        stub = get_stub()
        request = service_pb2.StatusRequest(appointment_id=id_consulta)
        response = stub.GetAppointmentStatus(request)
        
        if response.status == "Não encontrada":
             raise HTTPException(status_code=404, detail="Consulta inexistente no banco")
             
        return {
            "id_consulta": id_consulta, 
            "status": response.status
        }
    except grpc.RpcError as e:
        print(f"❌ Erro gRPC: {e}")
        raise HTTPException(status_code=503, detail="Falha na comunicacao com o servidor backend")

@app.put("/status/{id_consulta}")
async def atualizar_status(id_consulta: str, novo_status: str):
    # Endpoint para integracao com outros modulos do sistema distribuido
    try:
        stub = get_stub()
        request = service_pb2.UpdateStatusRequest(appointment_id=id_consulta, new_status=novo_status)
        response = stub.UpdateStatus(request)
        
        if response.status == "ERRO":
            raise HTTPException(status_code=400, detail=response.message)
            
        return {"id_consulta": id_consulta, "status": response.status, "mensagem": response.message}
    except grpc.RpcError:
        raise HTTPException(status_code=503, detail="Erro de rede ao atualizar status")