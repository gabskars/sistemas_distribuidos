import requests
import sys

def consultar_situacao(id_consulta):
    # Endereço da sua Interface REST
    url = f"http://localhost:8000/status/{id_consulta}"

    try:
        # Requisito: Comunicação direta via REST [cite: 27]
        response = requests.get(url)
        
        if response.status_code == 200:
            dados = response.json()
            print(f"🔍 CONSULTA ID: {dados['id_consulta']}")
            print(f"📊 STATUS ATUAL: {dados['status']}")
        else:
            print(f"❌ ERRO: {response.json().get('detail', 'Consulta não encontrada')}")
            
    except Exception as e:
        print(f"⚠️ Erro ao conectar na interface: {e}")

if __name__ == "__main__":
    # Uso: python status.py [ID_DA_CONSULTA]
    if len(sys.argv) == 2:
        consultar_situacao(sys.argv[1])
    else:
        print("Uso correto: python status.py [ID_DA_CONSULTA]")