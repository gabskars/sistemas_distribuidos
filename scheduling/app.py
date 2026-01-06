import uvicorn
from fastapi import FastAPI, HTTPException
import grpc
import os
import service_pb2
import service_pb2_grpc

app = FastAPI()


GRPC_HOST = os.getenv("GRPC_HOST", "localhost")

def get_stub():
    """Configuração do canal de comunicação gRPC"""
    channel = grpc.insecure_channel(f"{GRPC_HOST}:50051")
    return service_pb2_grpc.SchedulingServiceStub(channel)



@app.post("/agendar")
def agendar(paciente: str, medico: str, especialidade: str, horario: str):
    stub = get_stub()
    try:
        response = stub.CreateAppointment(service_pb2.AppointmentRequest(
            paciente=paciente, medico=medico, especialidade=especialidade, horario=horario
        ))
        if not response.sucesso:
            raise HTTPException(status_code=400, detail=response.mensagem)
        return {"id_consulta": response.id_consulta, "mensagem": response.mensagem}
    except grpc.RpcError:
        raise HTTPException(status_code=500, detail="Erro de conexão com o servidor gRPC")

@app.get("/status/{id}")
def ver_status(id: int):
    stub = get_stub()
    try:
        response = stub.GetStatus(service_pb2.StatusRequest(id_consulta=id))
        return {"status": response.status}
    except Exception:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")

@app.put("/confirmar/{id}")
def confirmar_consulta(id: int):
    stub = get_stub()
    try:
        response = stub.UpdateStatus(service_pb2.UpdateRequest(
            id_consulta=id, novo_status="Confirmada"
        ))
        if not response.sucesso:
            raise HTTPException(status_code=404, detail=response.mensagem)
        return {"mensagem": response.mensagem}
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao atualizar status via gRPC")

# --- CAMADA DE COMPATIBILIDADE  ---

@app.post("/appointments")
def schedule_legacy(data: dict):
    
    return agendar(
        paciente=data.get("paciente"),
        medico=data.get("medico"),
        especialidade=data.get("especialidade", "Geral"), 
        horario=data.get("horario")
    )


@app.get("/appointments")
def list_legacy():

    return {
        "aviso": "Sistema atualizado para persistência SQLite.",
        "instrucao": "Use /status/{id} para consultas individuais."
    }

if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=5000)
