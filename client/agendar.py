import requests
import sys

# O papel da interface é encaminhar requisições do Lado Cliente para o serviço
# Este script faz a comunicação direta via REST com a interface

def realizar_agendamento(paciente, medico, especialidade, data_hora):
    # A interface está rodando na porta 8000 (configurada no docker-compose/uvicorn)
    url = "http://localhost:8000/agendar"
    
    # Parâmetros que enviamos para a Interface REST
    params = {
        "paciente_id": paciente,
        "medico_id": medico,
        "especialidade": especialidade,
        "data_hora": data_hora
    }

    try:
        # Enviamos um POST para a interface
        response = requests.post(url, params=params)
        
        # Se a resposta for 200 (Sucesso)
        if response.status_code == 200:
            dados = response.json()
            print(f"✅ SUCESSO: {dados['mensagem']}")
            print(f"🆔 ID da Consulta: {dados['id_consulta']}")
            print(f"📊 Status: {dados['status']}")
        
        # Se houver erro (como conflito de horário ou erro no servidor)
        else:
            try:
                # Tenta ler o erro formatado em JSON enviado pelo FastAPI
                erro = response.json().get('detail', 'Erro desconhecido')
                print(f"❌ ERRO NO AGENDAMENTO: {erro}")
            except Exception:
                # Se o servidor cair ou retornar um erro estranho (HTML), mostra o texto puro
                print(f"❌ ERRO CRÍTICO NO SERVIDOR (Status {response.status_code}):")
                print(f"👉 {response.text[:200]}") # Mostra os primeiros 200 caracteres do erro

    except Exception as e:
        print(f"⚠️ Não foi possível conectar à Interface: {e}")

if __name__ == "__main__":
    # Verificamos se o usuário passou os 4 argumentos necessários via terminal
    # Exemplo de uso: python agendar.py "Ismael" "Dr_Filipe" "Cardio" "2026-01-10_14:00"
    if len(sys.argv) == 5:
        realizar_agendamento(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print("\n❌ ERRO: Faltam argumentos.")
        print("Uso correto: python agendar.py [NOME_PACIENTE] [ID_MEDICO] [ESPECIALIDADE] [DATA_HORA]")
        print("Exemplo: python agendar.py \"Ismael\" \"Dr_Filipe\" \"Sistemas\" \"2026-01-10_10:00\"")