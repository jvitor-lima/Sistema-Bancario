class Usuario:
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

    def get_nome(self):
        return self.nome

    def set_nome(self, nome):
        self.nome = nome

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def get_senha(self):
        return self.senha

    def set_senha(self, senha):
        self.senha = senha

    def __str__(self):
        return f'Nome: {self.nome}, Email: {self.email}'