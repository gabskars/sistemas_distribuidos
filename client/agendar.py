import requests
import sys

# O papel da interface é encaminhar requisições do Lado Cliente para o serviço [cite: 22]
# Este script faz a comunicação direta via REST com a interface 

def realizar_agendamento(paciente, medico, especialidade, data_hora):
    # A interface está rodando na porta 8000 (configurada no uvicorn)
    url = "http://localhost:8000/agendar"
    
    # Parâmetros que enviamos para a Interface REST
    params = {
        "paciente_id": paciente,
        "medico_id": medico,
        "especialidade": especialidade,
        "data_hora": data_hora
    }

    try:
        # Enviamos um POST para a interface [cite: 35]
        response = requests.post(url, params=params)
        
        if response.status_code == 200:
            dados = response.json()
            print(f"✅ SUCESSO: {dados['mensagem']}")
            print(f"🆔 ID da Consulta: {dados['id_consulta']}")
            print(f"📊 Status: {dados['status']}")
        else:
            # Caso ocorra o erro de conflito de horário que programamos no servidor
            erro = response.json().get('detail', 'Erro desconhecido')
            print(f"❌ ERRO NO AGENDAMENTO: {erro}")
            
    except Exception as e:
        print(f"⚠️ Não foi possível conectar à Interface: {e}")

if __name__ == "__main__":
    # Verificamos se o usuário passou todos os dados via terminal [cite: 88]
    # Exemplo de uso: python agendar.py "Ismael" "Dr_Filipe" "Cardio" "2026-01-10_14:00"
    if len(sys.argv) == 5:
        realizar_agendamento(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print("Uso correto: python agendar.py [NOME_PACIENTE] [ID_MEDICO] [ESPECIALIDADE] [DATA_HORA]")