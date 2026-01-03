import sqlite3

def init_db():
    # Conecta ao SQLite (arquivo persistido no volume do container)
    conn = sqlite3.connect('agendamentos.db')
    cursor = conn.cursor()
    
    # Cria o schema da tabela caso nao exista (garante idempotencia)
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
    print("✅ Banco de dados SQLite inicializado.")

if __name__ == '__main__':
    # Execucao isolada para criacao manual ou reset do banco
    init_db()