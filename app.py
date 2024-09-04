from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from usuario import Usuario
from conta import Conta, transferir
import json
import os

app = FastAPI()

contas = []
usuarios = []
import os

def carregar_dados():
    try:
        with open('usuarios.json', 'r') as f:
            usuarios_data = json.load(f)
            for usuario in usuarios_data:
                usuarios.append(Usuario(usuario['nome'], usuario['email'], usuario['senha']))

    except FileNotFoundError:
        print("Arquivo 'usuarios.json' não encontrado.")
        return

    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON no arquivo 'usuarios.json': {e}")
        return

    try:
        with open('contas.json', 'r') as f:
            contas_data = json.load(f)
            for conta in contas_data:
                email_conta = conta['usuario']['email'].strip().lower()  # Normalizando o e-mail aqui também
                usuario = next((u for u in usuarios if u.get_email() == email_conta), None)
                
                if usuario is None:
                    print(f"Usuário com e-mail {email_conta} não encontrado. Ignorando esta conta.")
                    continue
            
                nova_conta = Conta(usuario, conta['saldo'])
                nova_conta.numero = conta['numero']
                nova_conta.transacoes = conta['transacoes']
                contas.append(nova_conta)

    except FileNotFoundError:
        print("Arquivo 'contas.json' não encontrado.")

    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON no arquivo 'contas.json': {e}")

    except Exception as e:
        print(f"Erro inesperado: {e}")




carregar_dados()

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


# @app.get("/hello world")
# async def root():
#     return {"message": "Hello World"}



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


@app.put("/usuarios/{email}")
def atualizar_usuario(email: str, usuario: UsuarioModel):
    usuario_existente = next((u for u in usuarios if u.get_email() == email), None)
    if usuario_existente:
        usuario_existente.set_nome(usuario.nome)
        usuario_existente.set_email(usuario.email)
        usuario_existente.set_senha(usuario.senha)
        salvar_dados()
        return {"mensagem": "Usuário atualizado com sucesso!"}
    else:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    

@app.put("/contas/{numero}")
def atualizar_conta(numero: int, conta: ContaModel):
    conta_existente = next((c for c in contas if c.numero == numero), None)
    if conta_existente:
        conta_existente.usuario = next((u for u in usuarios if u.get_email() == conta.email), conta_existente.usuario)
        conta_existente.saldo = conta.saldo_inicial
        salvar_dados()
        return {"mensagem": "Conta atualizada com sucesso!"}
    else:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    

@app.delete("/usuarios/{email}")
def deletar_usuario(email: str):
    global usuarios
    usuarios = [u for u in usuarios if u.get_email() != email]
    salvar_dados()
    return {"mensagem": "Usuário deletado com sucesso!"}


@app.delete("/contas/{numero}")
def deletar_conta(numero: int):
    global contas
    contas = [c for c in contas if c.numero != numero]
    salvar_dados()
    return {"mensagem": "Conta deletada com sucesso!"}


@app.get("/usuarios")
def listar_usuarios():
    return [
        {
            "nome": usuario.get_nome(),
            "email": usuario.get_email(),
        }
        for usuario in usuarios
    ]

@app.get("/contas")
def listar_contas():
    print("Contas disponíveis:", contas)
    return [
        {
            "numero": conta.numero,
            "usuario": conta.usuario.get_nome(),
            "saldo": conta.get_saldo()
        }
        for conta in contas
    ]
# print("Diretório de trabalho atual:", os.getcwd())



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)