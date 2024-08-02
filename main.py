import json
from usuario import Usuario
from conta import Conta, transferir
# Lista de contas e usuários para armazenar todos os dados criados
contas = []
usuarios = []

# a função para carregar e salvar dados 
def carregar_dados():
    try:
        with open('usuarios.json', 'r') as f:
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
        usuarios_data = [{'Nome': u.get.nome(), 'E-mail': u.get.email(), 'Senha': u.get.senha()} for u in usuarios]
        json.dump(usuarios_data, f)
    with open('contas.json', 'w') as f:
        contas_data = [{
            'numero': c.numero,
            'usuario': {'nome': c.usuario.get_nome(), 'email': c.usuario.get_email(), 'senha': c.usuario.get_senha()},
            'saldo': c.get_saldo(),
            'transacoes': c.get_transacoes()
        } for c in contas]
        json.dump(contas_data, f)   
        
def criar_usuario():
    nome = input("Digite o nome do usuário: ")
    email = input("Digite o e-mail do usuário: ")
    senha = input("Digite a senha do usuário: ")
    usuario = Usuario(nome, email, senha)
    usuarios.append(usuario)
    return usuario
    

def criar_conta():
    usuario = criar_conta()
    saldo_inicial = float(input("Digite o saldo inicial: "))
    conta = conta(usuario, saldo_inicial)
    contas.append(conta)
    print(f"Conta criada com sucesso! Número da conta: {conta.numero}")

def encotrar_conta():
    numero = int(input('Digite o número da conta: '))
    for conta in contas:
        if conta.numero == numero:
            return conta
    print(f"Está conta: {numero}, não consta no nosso banco! Por favor, insira um número válido.")
    return None
def autenticar_usuario():
    email = input("Digite o e-mail: ")
    senha = input("Digite a senha: ")
    for usuario in usuarios:
        if usuario.get_email() == email and usuario.get_senha() == senha:
            print(f"Usuário {usuario.get_nome()} autenticado com sucesso!")
            return usuario
    print("Email ou senha inválidos")
    return None


def Menu():
    carregar_dados()
    usuario_autenticado = None
    while True:
        if not usuario_autenticado:
            print("n\---- MENU DE AUTENTICAÇÃO ----")
            print("1. LOGIN")
            print("2. CRIAR CONTA")
            print("3. SAIR")
            opcao = int(input("Escolha uma opção: "))

        if opcao == 1:
            usuario_autenticado = autenticar_usuario()
        elif opcao == 2:
            criar_conta()
        elif opcao == 3:
            salvar_dados()
            print('Saindo...')
            break
        else:
            print("Opção inválida. Tente novamente")

    
    else:
        print(f"\nBem-vindo, {usuario_autenticado.get_nome()}!")
        print("\n----- Menu -----")
        print("1. Depositar")
        print("2. Sacar")
        print("3. Transferir")
        print("4. Ver saldo")
        print("5. Ver histórico de transações")
        print("6. Logout")
        print("7. Sair")
        opcao = int(input("Escolha uma opção: "))

        if opcao == 1:
            conta = encontrar_conta()
            if conta and conta_usuario == usuario_autenticado:
                valor = float(input("Digite o valor para depositar: "))
                conta.depositar(valor)
        elif opcao == 2:
            if conta and conta_usuario == usuario_autenticado:
                valor = float(input("Digite o valor para sacar: "))
                canta.sacar(valor)

        elif opcao == 3:
            conta_origem = encontrar_conta()
            if conta_origem and conta_origem.usuario == usuario_autenticado:
                conta_destino = encotrar_conta()
                if conta_destino:
                    valor = float(input("Digite o valor para transferir: "))
                    transferir(conta_origem, conta_destino, valor)

        elif opcao == 4:
            conta = encontrar_conta()
            if conta and conta_usuario == usuario_autenticado:
                print(f"Saldo: R${conta.get_saldo():.2f}")

        elif opcao == 5:
            conta = encontrar_conta()
            if conta and conta_usuario == usuario_autenticado:
                for transacao in conta.get_transacoes():
                    print(transacao)
            
        elif opcao == 6:
            print("Logout realizado com sucesso!!!")
            usuario_autenticado = None

        else:
            print("Opção inválida. Tente novamente!")

if __name__ == "__main__":
    Menu()
