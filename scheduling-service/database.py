import sqlite3

def init_db():
    # Conecta ao arquivo de banco de dados (será criado na raiz /app/ dentro do Docker)
    conn = sqlite3.connect('agendamentos.db')
    cursor = conn.cursor()
    
    # Cria a tabela de consultas se ela ainda não existir
    # A estrutura está perfeitamente alinhada com as chamadas gRPC do app.py
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id TEXT NOT NULL,
            medico_id TEXT NOT NULL,
            especialidade TEXT NOT NULL,
            data_hora TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Banco de dados SQLite inicializado (agendamentos.db).")

if __name__ == '__main__':
    # Permite rodar este script isoladamente para resetar/criar o banco
    init_db()