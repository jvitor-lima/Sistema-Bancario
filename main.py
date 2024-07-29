from usuario import Usuario
from conta import Conta
    
Usuario1 = Usuario("Vitor", "Vitor@gmail.com", "12345678")
print(Usuario1)

conta1 = Conta(Usuario1, 1.000)
print(conta1)

usuario2 = Usuario("Rodrigo", "Rodrigo@hotmail.com", "5555")
conta2 = Conta(usuario2, 500.0)
print(conta2)