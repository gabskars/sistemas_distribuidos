import requests
import sys

def atualizar_status(id_consulta, novo_status):
    # Endpoint PUT definido na Interface
    url = f"http://localhost:8000/status/{id_consulta}"
    params = {"novo_status": novo_status}

    try:
        # Chamada PUT para atualizar o recurso
        response = requests.put(url, params=params)
        
        if response.status_code == 200:
            dados = response.json()
            print(f"✅ SUCESSO: {dados['mensagem']}")
            print(f"📊 NOVO STATUS: {dados['status']}")
        else:
            try:
                erro = response.json().get('detail', 'Erro ao atualizar.')
                print(f"❌ ERRO: {erro}")
            except:
                print(f"❌ ERRO NO SERVIDOR: {response.status_code}")

    except Exception as e:
        print(f"⚠️ Erro de conexão: {e}")

if __name__ == "__main__":
    # Espera ID da consulta e o novo status
    if len(sys.argv) == 3:
        atualizar_status(sys.argv[1], sys.argv[2])
    else:
        print("\n❌ ERRO: Argumentos faltando.")
        print("Uso: python atualizar.py [ID] [NOVO_STATUS]")
        print("Ex: python atualizar.py 1 Confirmada")