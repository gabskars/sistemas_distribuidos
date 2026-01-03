import requests
import sys

def consultar_situacao(id_consulta):
    # Endpoint da API configurado no docker-compose
    url = f"http://localhost:8000/status/{id_consulta}"

    try:
        # Chamada GET para consultar o ID no banco via interface
        response = requests.get(url)
        
        # 200 OK: ID localizado no SQLite via gRPC
        if response.status_code == 200:
            dados = response.json()
            print("\n--- 🔍 DETALHES DA CONSULTA ---")
            print(f"🆔 ID: {dados['id_consulta']}")
            print(f"📊 STATUS ATUAL: {dados['status']}")
            print("-------------------------------\n")
        
        # Trata erros da API (404 Not Found ou 500 Internal Error)
        else:
            try:
                # Tenta capturar a mensagem de erro da FastAPI
                erro_msg = response.json().get('detail', 'Consulta não localizada.')
                print(f"❌ ERRO: {erro_msg}")
            except Exception:
                # Fallback para erros brutos do servidor
                print(f"❌ ERRO NO SERVIDOR (Status {response.status_code})")
                print(f"👉 Info técnica: {response.text[:100]}")
            
    except Exception as e:
        print(f"⚠️ Erro de conexão: Verifique se o Docker está rodando.")

if __name__ == "__main__":
    # Script espera o ID da consulta como argumento de linha de comando
    if len(sys.argv) == 2:
        consultar_situacao(sys.argv[1])
    else:
        print("\n❌ ERRO: Informe o ID da consulta.")
        print("Exemplo: python status.py 1")