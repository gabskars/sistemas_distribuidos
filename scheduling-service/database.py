import sqlite3

def init_db():
    # Conecta ao arquivo de banco de dados (se não existir, ele cria)
    conn = sqlite3.connect('agendamentos.db')
    cursor = conn.cursor()
    
    # Cria a tabela de consultas se ela ainda não existir
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
    print("Banco de dados inicializado com sucesso!")

if __name__ == '__main__':
    init_db()