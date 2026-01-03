import requests
import sys

# Script do Lado Cliente para consultar a situação de um agendamento
# Realiza comunicação direta via REST com a Interface de Agendamento

def consultar_situacao(id_consulta):
    # Endereço da Interface REST (API Gateway)
    # Porta 8000 mapeada no Docker para acesso externo
    url = f"http://localhost:8000/status/{id_consulta}"

    try:
        # Requisito: Operação de consulta via método GET
        response = requests.get(url)
        
        # Se a consulta for encontrada com sucesso
        if response.status_code == 200:
            dados = response.json()
            print("\n--- 🔍 DETALHES DA CONSULTA ---")
            print(f"🆔 ID: {dados['id_consulta']}")
            print(f"📊 STATUS ATUAL: {dados['status']}")
            print("-------------------------------\n")
        
        # Tratamento de erro (Ex: ID não encontrado ou erro no servidor)
        else:
            try:
                # Tenta extrair a mensagem de erro formatada pela API
                erro_msg = response.json().get('detail', 'Consulta não localizada.')
                print(f"❌ ERRO: {erro_msg}")
            except Exception:
                # Caso o servidor retorne um erro bruto (HTML/Texto)
                print(f"❌ ERRO NO SERVIDOR (Status {response.status_code})")
                print(f"👉 Detalhe técnico: {response.text[:150]}")
            
    except Exception as e:
        print(f"⚠️ Falha de conexão: Não foi possível alcançar a Interface REST.")
        print(f"👉 Verifique se os containers Docker estão rodando.")

if __name__ == "__main__":
    # O sistema espera exatamente 1 argumento: o ID da consulta
    # Exemplo: python status.py 4
    if len(sys.argv) == 2:
        consultar_situacao(sys.argv[1])
    else:
        print("\n❌ ERRO: ID da consulta não informado.")
        print("Uso correto: python status.py [ID_DA_CONSULTA]")
        print("Exemplo: python status.py 10")