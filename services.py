from models import UsuarioModel, ContaModel, TransacaoModel, TransferenciaModel
from database import (
    inserir_usuario, inserir_conta, inserir_transacao, buscar_usuario,
    buscar_conta, buscar_contas_usuario, buscar_transacoes, atualizar_saldo
)

def criar_usuario(usuario: UsuarioModel):
    if buscar_usuario(usuario.email):
        raise ValueError("Usuário já existe")
    inserir_usuario(usuario.nome, usuario.email, usuario.senha)

def criar_conta(conta: ContaModel):
    if not buscar_usuario(conta.email):
        raise ValueError("Usuário não encontrado")
    inserir_conta(conta.email, conta.saldo_inicial)

def depositar(numero_conta: int, valor: float):
    conta = buscar_conta(numero_conta)
    if not conta:
        raise ValueError("Conta não encontrada")
    novo_saldo = conta[2] + valor
    atualizar_saldo(numero_conta, novo_saldo)
    inserir_transacao(numero_conta, "Deposito", valor)

def sacar(numero_conta: int, valor: float):
    conta = buscar_conta(numero_conta)
    if not conta:
        raise ValueError("Conta não encontrada")
    saldo_atual = conta[2]
    if saldo_atual < valor:
        raise ValueError("Saldo insuficiente")
    novo_saldo = saldo_atual - valor
    atualizar_saldo(numero_conta, novo_saldo)
    inserir_transacao(numero_conta, "Saque", valor)

def transferir(conta_origem: int, conta_destino: int, valor: float):
    saldo_origem = buscar_conta(conta_origem)[2]
    if saldo_origem < valor:
        raise ValueError("Saldo insuficiente")
    sacar(conta_origem, valor)
    depositar(conta_destino, valor)
    inserir_transacao(conta_origem, "Transferência", -valor)
    inserir_transacao(conta_destino, "Transferência", valor)
