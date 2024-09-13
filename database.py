import sqlite3

def get_connection():
    return sqlite3.connect('SistemaBancario.db')

def inicializar_bd():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                saldo REAL NOT NULL,
                tipo INTEGER NOT NULL CHECK(tipo IN (1, 2)),  -- 1 para conta corrente, 2 para conta poupança
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transferencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conta_origem_id INTEGER NOT NULL,
                conta_destino_id INTEGER NOT NULL,
                valor REAL NOT NULL,
                data TEXT NOT NULL,
                FOREIGN KEY (conta_origem_id) REFERENCES contas (id),
                FOREIGN KEY (conta_destino_id) REFERENCES contas (id)
            )
        """)
        conn.commit()
    finally:
        conn.close()
