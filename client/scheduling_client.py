import requests

URL_BASE = "http://scheduling:5000"

def agendar_consulta(paciente, medico, especialidade, horario):
    url = f"{URL_BASE}/agendar"
    params = {
        "paciente": paciente,
        "medico": medico,
        "especialidade": especialidade,
        "horario": horario
    }
    
    try:
        response = requests.post(url, params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Agendamento realizado! ID: {data.get('id_consulta')}")
        else:
            print(f"❌ Erro ao agendar: {response.json().get('detail')}")
    except Exception as e:
        print(f"⚠️ Erro de conexão: {e}")

def consultar_status(id_consulta):
    url = f"{URL_BASE}/status/{id_consulta}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"ℹ️ Status da Consulta {id_consulta}: {response.json().get('status')}")
        else:
            print(f"❌ Consulta não encontrada.")
    except Exception as e:
        print(f"⚠️ Erro de conexão: {e}")

def confirmar_agendamento(id_consulta):
    url = f"{URL_BASE}/confirmar/{id_consulta}"

    try:
        # PUT para atualizações de status
        response = requests.put(url)
        if response.status_code == 200:
            print(f"✅ Sucesso: {response.json().get('mensagem')}")
        else:
            print(f"❌ Erro ao confirmar: {response.json().get('detail')}")
    except Exception as e:
        print(f"⚠️ Erro de conexão: {e}")

if __name__ == "__main__":
    print("\n--- SISTEMA DE AGENDAMENTO (CLIENTE) ---")
    print("1. Agendar nova consulta")
    print("2. Verificar status")
    print("3. Confirmar consulta (Validar)")
    print("4. Sair")

    opcao = input("\nEscolha uma opção: ")

    if opcao == "1":
        p = input("Nome do Paciente: ")
        m = input("Nome do Médico: ")
        e = input("Especialidade: ")
        h = input("Horário (Ex: 2026-01-10 14:00): ")
        agendar_consulta(p, m, e, h)
    
    elif opcao == "2":
        id_c = input("ID da Consulta: ")
        consultar_status(id_c)
        
    elif opcao == "3":
        id_c = input("ID da consulta para confirmar: ")
        confirmar_agendamento(id_c)
    
    elif opcao == "4":
        print("Saindo...")