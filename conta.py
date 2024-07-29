class Conta:
    contador_contas = 10

    def __init__(self, usuario, saldo=0.0):
        Conta.contador_contas += 10
        self.numero = Conta.contador_contas  
        self.usuario = usuario
        self.saldo = saldo
        self.transacoes = []

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.transacoes.append(f"Deposito: R${valor:.2f}")
        else:
            print("Valor de depósito inválido")

    def sacar(self, valor):
        if 0 < valor <= self.saldo:
            self.saldo -= valor
            self.transacoes.append(f"Saque: R${valor:.2f}")
        else:
            print("Saldo insuficiente ou valor de saque inválido")

    def get_saldo(self):
        return self.saldo

    def get_transacoes(self):
        return self.transacoes

    def __str__(self):
        return f'Conta: {self.numero}, Usuario: {self.usuario.nome}, Saldo: R${self.saldo:.2f}'

def transferir(conta_origem, conta_destino, valor):
    if conta_origem.saldo >= valor:
        conta_origem.sacar(valor)
        conta_destino.depositar(valor)
        conta_origem.transacoes.append(f"Transferência para a conta {conta_destino.numero}: R${valor:.2f}")
        conta_destino.transacoes.append(f"Transferência para a conta {conta_origem.numero}: R${valor:.2f}")

    else:
        print("Saldo insuficiente para a transferência")

