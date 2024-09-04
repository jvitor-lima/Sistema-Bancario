import re

class Usuario:
    def __init__(self, nome, email, senha):
        self.set_nome(nome)
        self.email = email.strip().lower()  
        self.set_senha(senha)


    def set_nome(self, nome):
        self.nome = nome

    def set_email(self, email):
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.email = email
        else:
            raise ValueError("E-mail inválido")
   
    def set_senha(self, senha):
        if len(senha) >= 8:
            self.senha = senha
        else:
            raise ValueError("Senha deve ter pelo menos 8 caracteres")


    def get_nome(self):
        return self.nome

    def get_email(self):
        return self.email

    def get_senha(self):
        return self.senha

    def __str__(self):
        return f'Nome: {self.nome}, Email: {self.email}'
