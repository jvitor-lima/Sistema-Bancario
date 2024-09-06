import sqlite3

# Nome do banco de dados
DB_NAME = "banco.db"

def get_connection():
    """
    Retorna uma conexão com o banco de dados SQLite.
    """
    return sqlite3.connect(DB_NAME)

def inicializar_bd():
    """
    Cria as tabelas necessárias no banco de dados, se não existirem.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Criação da tabela de usuários
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )
    """)

    # Criação da tabela de contas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contas (
        numero INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        saldo REAL NOT NULL,
        FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
    )
    """)

    # Criação da tabela de transações (adicionado, já que você mencionou)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_conta INTEGER NOT NULL,
        tipo TEXT NOT NULL,
        valor REAL NOT NULL,
        FOREIGN KEY (numero_conta) REFERENCES contas (numero)
    )
    """)

    conn.commit()
    conn.close()

def inserir_usuario(nome, email, senha):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)', (nome, email, senha))
    conn.commit()
    conn.close()

def inserir_conta(email_usuario, saldo):
    conn = get_connection()
    cursor = conn.cursor()
    usuario = buscar_usuario(email_usuario)
    if usuario:
        cursor.execute('INSERT INTO contas (usuario_id, saldo) VALUES (?, ?)', (usuario[0], saldo))
        conn.commit()
    conn.close()

def inserir_transacao(numero_conta, tipo, valor):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO transacoes (numero_conta, tipo, valor) VALUES (?, ?, ?)', (numero_conta, tipo, valor))
    conn.commit()
    conn.close()

def buscar_usuario(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

def buscar_conta(numero):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contas WHERE numero = ?', (numero,))
    conta = cursor.fetchone()
    conn.close()
    return conta

def buscar_contas_usuario(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contas WHERE usuario_id = (SELECT id FROM usuarios WHERE email = ?)', (email,))
    contas = cursor.fetchall()
    conn.close()
    return contas

def buscar_transacoes(numero_conta):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT tipo, valor FROM transacoes WHERE numero_conta = ?', (numero_conta,))
    transacoes = cursor.fetchall()
    conn.close()
    return transacoes

def atualizar_saldo(numero_conta, saldo):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE contas SET saldo = ? WHERE numero = ?', (saldo, numero_conta))
    conn.commit()
    conn.close()
