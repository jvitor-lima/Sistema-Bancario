from pydantic import BaseModel

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
