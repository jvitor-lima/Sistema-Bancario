from fastapi import FastAPI, HTTPException
import requests
from Usuario import Usuario
from ContaBancaria import ContaBancaria
from Transferencia import Transferencia
from database import inicializar_bd

app = FastAPI()
dolar = "https://economia.awesomeapi.com.br/json/last/USD-BRL"

@app.post("/usuarios/")
async def criar_usuario(nome: str, cpf: str, email: str, senha: str):
    Usuario.criar_usuario(nome, cpf, email, senha)
    return {"status": "Usuário criado com sucesso"}

@app.get("/usuarios/{id}")
async def buscar_usuario(id: int):
    usuario = Usuario.buscar_usuario(id)
    if usuario:
        return usuario
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

@app.put("/usuarios/{id}")
async def atualizar_usuario(id: int, nome: str, cpf: str, email: str, senha: str):
    Usuario.atualizar_usuario(id, nome, cpf, email, senha)
    return {"status": "Usuário atualizado com sucesso"}

@app.delete("/usuarios/{id}")
async def deletar_usuario(id: int):
    Usuario.deletar_usuario(id)
    return {"status": "Usuário deletado com sucesso"}

@app.post("/contas/")
async def criar_conta(usuario_id: int, saldo: float, tipo: int):
    try:
        ContaBancaria.criar_conta(usuario_id, saldo, tipo)
        return {"status": "Conta criada com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/contas/{id}")
async def buscar_conta(id: int):
    conta = ContaBancaria.buscar_conta(id)
    if conta:
        return conta
    raise HTTPException(status_code=404, detail="Conta não encontrada")


@app.get("/usuarios/{usuario_id}/contas")
async def listar_contas_por_usuario(usuario_id: int):
    contas = ContaBancaria.listar_contas_por_usuario(usuario_id)
    if not contas:
        raise HTTPException(status_code=404, detail="Nenhuma conta encontrada para este usuário.")
    return {"contas": contas}


@app.delete("/contas/{id}/encerrar")
async def encerrar_conta(id: int):
    try:
        ContaBancaria.encerrar_conta(id)
        return {"status": "Conta encerrada com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@app.get("/cotacaoDolar")
def listar_dolar():
    response = requests.get(dolar)

    if response.status_code == 200:
        data = response.json()
        cotacao_dolar = data["USDBRL"]
        
        return {
            "nome": cotacao_dolar["name"],
            "compra": cotacao_dolar["bid"],
            "venda": cotacao_dolar["ask"],
        }
    else:
        return {"erro": "Falha ao consultar a cotação do dólar"}

@app.post("/transferencias/")
async def realizar_transferencia(conta_origem_id: int, conta_destino_id: int, valor: float):
    try:
        Transferencia.realizar_transferencia(conta_origem_id, conta_destino_id, valor)
        return {"status": "Transferência realizada com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/transferencias/")
async def listar_transferencias(conta_origem_id: int = None, conta_destino_id: int = None):
    transferencias = Transferencia.listar_transferencias(conta_origem_id, conta_destino_id)
    return {"transferencias": transferencias}


if __name__ == "__main__":
    inicializar_bd()
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
