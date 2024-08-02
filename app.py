from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from usuario import Usuario
from conta import Conta, transferir
import json


app = FastAPI()

contas = []
usuario = []

def carregar_dados():
    try:
        with open('usuario.json', 'r') as f:
            usuarios_data = json.load(f)
            for usuario in usuarios_data:
                usuarios.append(Usuario(usuario['nome'], usuario['email'], usuario['senha']))
        with open('contas.json', 'r') as f:
            contas_data = json.load(f)
            for conta in contas_data:
                usuario = next(u for u in usuarios if u.get_email() == conta['usuario']['email'])
                nova_conta = Conta(usuario, conta['saldo'])
                nova_conta.numero = conta['numero']
                nova_conta.transacoes = conta['transacoes']
                contas.append(nova_conta)
    except FileNotFoundError:
        pass

def salvar_dados():
    with open('usuarios.json', 'w') as f:
        usuarios_data = [{'nome': u.get_nome(), 'email': u.get_email(), 'senha': u.get_senha()} for u in usuarios]
        json.dump(usuarios_data, f)
    with open('contas.json', 'w') as f:
        contas_data = [{
            'numero': c.numero,
            'usuario': {'nome': c.usuario.get_nome(), 'email': c.usuario.get_email(), 'senha': c.usuario.get_senha()},
            'saldo': c.get_saldo(),
            'transacoes': c.get_transacoes()
        } for c in contas]
        json.dump(contas_data, f)

carregar_dados()

class UsuarioModel(BaseModel):
    nome: str
    email: str
    senha: str

class ContaModel(BaseModel):
    email: str
    saldo_inicial: float = 0.0

class TransacaoModel(BaseModel):
    valor: float

class TransferenciaModel(BaseModel):
    conta_origem: int
    conta_destino: int
    valor: float

@app.post("/usuarios")
def criar_usuario(usuario: UsuarioModel):
    try:
        novo_usuario = Usuario(usuario.nome, usuario.email, usuario.senha)
        usuarios.append(novo_usuario)
        salvar_dados()
        return {"mensagem": "Usuário criado com sucesso!"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/contas")
def criar_conta(conta: ContaModel):
    usuario = next((u for u in usuarios if u.get_email() == conta.email), None)
    if usuario:
        nova_conta = Conta(usuario, conta.saldo_inicial)
        contas.append(nova_conta)
        salvar_dados()
        return {"mensagem": "Conta criada com sucesso!", "numero_conta": nova_conta.numero}
    else:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

@app.get("/contas/{numero}")
def obter_conta(numero: int):
    conta = next((c for c in contas if c.numero == numero), None)
    if conta:
        return {
            "numero": conta.numero,
            "usuario": conta.usuario.get_nome(),
            "saldo": conta.get_saldo(),
            "transacoes": conta.get_transacoes()
        }
    else:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

@app.post("/contas/{numero}/depositar")
def depositar(numero: int, transacao: TransacaoModel):
    conta = next((c for c in contas if c.numero == numero), None)
    if conta:
        conta.depositar(transacao.valor)
        salvar_dados()
        return {"mensagem": "Depósito realizado com sucesso!"}
    else:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

@app.post("/contas/{numero}/sacar")
def sacar(numero: int, transacao: TransacaoModel):
    conta = next((c for c in contas if c.numero == numero), None)
    if conta:
        conta.sacar(transacao.valor)
        salvar_dados()
        return {"mensagem": "Saque realizado com sucesso!"}
    else:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

@app.post("/contas/transferir")
def realizar_transferencia(transferencia: TransferenciaModel):
    conta_origem = next((c for c in contas if c.numero == transferencia.conta_origem), None)
    conta_destino = next((c for c in contas if c.numero == transferencia.conta_destino), None)
    if conta_origem and conta_destino:
        transferir(conta_origem, conta_destino, transferencia.valor)
        salvar_dados()
        return {"mensagem": "Transferência realizada com sucesso!"}
    else:
        raise HTTPException(status_code=404, detail="Conta de origem ou destino não encontrada")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)