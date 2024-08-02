
import unittest
from usuario import Usuario
from conta import Conta, transferir

class TestSistemaBancario(unittest.TestCase):

    def setUp(self):
        self.usuario1 = Usuario("Vitor", "Vitor@gmail.com", "senha1234")
        self.usuario2 = Usuario("Rodrigo", "Rodrigo@hotmail.com", "senha5678")
        self.conta1 = Conta(self.usuario1, 1000.0)
        self.conta2 = Conta(self.usuario2, 500.0)

    def test_criar_usuario(self):
        self.assertEqual(self.usuario1.get_nome(), "Vitor")
        self.assertEqual(self.usuario1.get_email(), "Vitor@gmail.com")
        self.assertTrue(self.usuario1.validar_senha("senha1234"))

    def test_criar_conta(self):
        self.assertEqual(self.conta1.usuario, self.usuario1)
        self.assertEqual(self.conta1.get_saldo(), 1000.0)

    def test_depositar(self):
        self.conta1.depositar(500.0)
        self.assertEqual(self.conta1.get_saldo(), 1500.0)

    def test_sacar(self):
        self.conta1.sacar(200.0)
        self.assertEqual(self.conta1.get_saldo(), 800.0)

    def test_transferir(self):
        transferir(self.conta1, self.conta2, 300.0)
        self.assertEqual(self.conta1.get_saldo(), 700.0)
        self.assertEqual(self.conta2.get_saldo(), 800.0)

    def test_historico_transacoes(self):
        self.conta1.depositar(100.0)
        self.conta1.sacar(50.0)
        transferir(self.conta1, self.conta2, 100.0)
        transacoes = self.conta1.get_transacoes()
        self.assertIn("Depósito: R$100.00", transacoes)
        self.assertIn("Saque: R$50.00", transacoes)
        self.assertIn("Transferência para Conta 20: R$100.00", transacoes)

if __name__ == '__main__':
    unittest.main()
