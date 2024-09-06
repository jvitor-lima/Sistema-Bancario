from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import database

app = FastAPI()

# Modelos Pydantic
class UsuarioModel(BaseModel):
    nome: str
    email: str
    senha: str

class ContaModel(BaseModel):
    email: str
    saldo_inicial: float

class TransacaoModel(BaseModel):
    valor: float

class TransferenciaModel(BaseModel):
    conta_origem: int
    conta_destino: int
    valor: float

# Funções auxiliares
def get_usuario_by_email(email: str):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row
    return None

def get_conta_by_numero(numero: int):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contas WHERE numero = ?", (numero,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row
    return None

def create_usuario(usuario: UsuarioModel):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", 
                   (usuario.nome, usuario.email, usuario.senha))
    conn.commit()
    conn.close()

def create_conta(conta: ContaModel):
    conn = database.get_connection()
    cursor = conn.cursor()
    usuario = get_usuario_by_email(conta.email)
    if usuario:
        cursor.execute("INSERT INTO contas (usuario_id, saldo) VALUES (?, ?)",
                       (usuario[0], conta.saldo_inicial))
        conn.commit()
        conn.close()
        return cursor.lastrowid
    conn.close()
    return None

def depositar_conta(numero: int, valor: float):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE contas SET saldo = saldo + ? WHERE numero = ?", 
                   (valor, numero))
    conn.commit()
    conn.close()

def sacar_conta(numero: int, valor: float):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE contas SET saldo = saldo - ? WHERE numero = ?", 
                   (valor, numero))
    conn.commit()
    conn.close()

def transferir_conta(conta_origem: int, conta_destino: int, valor: float):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE contas SET saldo = saldo - ? WHERE numero = ?", 
                   (valor, conta_origem))
    cursor.execute("UPDATE contas SET saldo = saldo + ? WHERE numero = ?", 
                   (valor, conta_destino))
    conn.commit()
    conn.close()

@app.post("/usuarios")
def criar_usuario(usuario: UsuarioModel):
    try:
        create_usuario(usuario)
        return {"mensagem": "Usuário criado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/contas")
def criar_conta(conta: ContaModel):
    conta_id = create_conta(conta)
    if conta_id:
        return {"mensagem": "Conta criada com sucesso!", "numero_conta": conta_id}
    else:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

@app.get("/contas/{numero}")
def obter_conta(numero: int):
    conta = get_conta_by_numero(numero)
    if conta:
        return {
            "numero": conta[0],
            "usuario_id": conta[1],
            "saldo": conta[2],
            # Aqui você pode adicionar transações se estiver implementado
        }
    else:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

@app.post("/contas/{numero}/depositar")
def depositar(numero: int, transacao: TransacaoModel):
    conta = get_conta_by_numero(numero)
    if conta:
        depositar_conta(numero, transacao.valor)
        return {"mensagem": "Depósito realizado com sucesso!"}
    else:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

@app.post("/contas/{numero}/sacar")
def sacar(numero: int, transacao: TransacaoModel):
    conta = get_conta_by_numero(numero)
    if conta:
        sacar_conta(numero, transacao.valor)
        return {"mensagem": "Saque realizado com sucesso!"}
    else:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

@app.post("/contas/transferir")
def realizar_transferencia(transferencia: TransferenciaModel):
    conta_origem = get_conta_by_numero(transferencia.conta_origem)
    conta_destino = get_conta_by_numero(transferencia.conta_destino)
    if conta_origem and conta_destino:
        transferir_conta(transferencia.conta_origem, transferencia.conta_destino, transferencia.valor)
        return {"mensagem": "Transferência realizada com sucesso!"}
    else:
        raise HTTPException(status_code=404, detail="Conta de origem ou destino não encontrada")

@app.put("/usuarios/{email}")
def atualizar_usuario(email: str, usuario: UsuarioModel):
    try:
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET nome = ?, senha = ? WHERE email = ?", 
                       (usuario.nome, usuario.senha, email))
        conn.commit()
        conn.close()
        return {"mensagem": "Usuário atualizado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/contas/{numero}")
def atualizar_conta(numero: int, conta: ContaModel):
    try:
        conn = database.get_connection()
        cursor = conn.cursor()
        usuario = get_usuario_by_email(conta.email)
        if usuario:
            cursor.execute("UPDATE contas SET usuario_id = ?, saldo = ? WHERE numero = ?", 
                           (usuario[0], conta.saldo_inicial, numero))
            conn.commit()
            conn.close()
            return {"mensagem": "Conta atualizada com sucesso!"}
        else:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/usuarios/{email}")
def deletar_usuario(email: str):
    try:
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE email = ?", (email,))
        conn.commit()
        conn.close()
        return {"mensagem": "Usuário deletado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/contas/{numero}")
def deletar_conta(numero: int):
    try:
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contas WHERE numero = ?", (numero,))
        conn.commit()
        conn.close()
        return {"mensagem": "Conta deletada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/usuarios")
def listar_usuarios():
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, email FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return [{"nome": usuario[0], "email": usuario[1]} for usuario in usuarios]

@app.get("/contas")
def listar_contas():
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT numero, usuario_id, saldo FROM contas")
    contas = cursor.fetchall()
    conn.close()
    return [{"numero": conta[0], "usuario_id": conta[1], "saldo": conta[2]} for conta in contas]
