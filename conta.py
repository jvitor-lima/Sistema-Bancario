class Conta:
    contador_contas = 10

    def __init__(self, usuario, saldo=0.0):
        Conta.contador_contas += 10
        self.numero = Conta.contador_contas  
        self.usuario = usuario
        self.saldo = saldo

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
        else:
            print("Valor de depósito inválido")

    def sacar(self, valor):
        if 0 < valor <= self.saldo:
            self.saldo -= valor
        else:
            print("Saldo insuficiente ou valor de saque inválido")

    def get_saldo(self):
        return self.saldo

    def __str__(self):
        return f'Conta: {self.numero}, Usuario: {self.usuario.nome}, Saldo: R${self.saldo:.2f}'

