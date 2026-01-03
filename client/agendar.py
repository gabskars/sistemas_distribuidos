import requests
import sys

def realizar_agendamento(paciente, medico, especialidade, data_hora):
    # Endpoint da Interface REST (FastAPI)
    url = "http://localhost:8000/agendar"
    
    params = {
        "paciente_id": paciente,
        "medico_id": medico,
        "especialidade": especialidade,
        "data_hora": data_hora
    }

    try:
        response = requests.post(url, params=params)
        
        # Status 200: Agendamento confirmado pelo gRPC e salvo no banco
        if response.status_code == 200:
            dados = response.json()
            print(f"✅ SUCESSO: {dados['mensagem']}")
            print(f"🆔 ID da Consulta: {dados['id_consulta']}")
            print(f"📊 Status: {dados['status']}")
        
        # Erros de validação ou conflito de horário (400 Bad Request)
        else:
            try:
                erro = response.json().get('detail', 'Erro desconhecido')
                print(f"❌ ERRO NO AGENDAMENTO: {erro}")
            except Exception:
                # Caso o servidor retorne um erro bruto (HTML/Text)
                print(f"❌ ERRO CRÍTICO NO SERVIDOR (Status {response.status_code})")
                print(f"👉 Detalhes: {response.text[:150]}")

    except Exception as e:
        print(f"⚠️ Erro de conexão com a Interface: {e}")

if __name__ == "__main__":
    # Espera 4 argumentos: paciente, medico, especialidade, data_hora
    if len(sys.argv) == 5:
        realizar_agendamento(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print("\n❌ ERRO: Faltam argumentos.")
        print("Uso: python agendar.py [PACIENTE] [MEDICO] [ESPECIALIDADE] [DATA_HORA]")
        print("Ex: python agendar.py \"Ismael\" \"Dr_Filipe\" \"Sistemas\" \"2026-01-10_10:00\"")