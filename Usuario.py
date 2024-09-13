from database import get_connection

class Usuario:
    def __init__(self, nome: str, cpf: str, email: str, senha: str):
        self.__nome = nome
        self.__cpf = cpf
        self.__email = email
        self.__senha = senha

    def get_nome(self) -> str:
        return self.__nome

    def get_cpf(self) -> str:
        return self.__cpf

    def get_email(self) -> str:
        return self.__email

    def get_senha(self) -> str:
        return self.__senha

    def set_nome(self, nome: str):
        self.__nome = nome

    def set_cpf(self, cpf: str):
        self.__cpf = cpf

    def set_email(self, email: str):
        self.__email = email

    def set_senha(self, senha: str):
        self.__senha = senha

    @staticmethod
    def criar_usuario(nome: str, cpf: str, email: str, senha: str):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO usuarios (nome, cpf, email, senha) VALUES (?, ?, ?, ?)
            """, (nome, cpf, email, senha))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def buscar_usuario(id: int):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
            usuario = cursor.fetchone()
            if usuario:
                return {
                    "id": usuario[0],
                    "nome": usuario[1],
                    "cpf": usuario[2],
                    "email": usuario[3],
                    "senha": usuario[4]
                }
            else:
                return None
        finally:
            conn.close()

    @staticmethod
    def atualizar_usuario(id: int, nome: str, cpf: str, email: str, senha: str):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE usuarios SET nome = ?, cpf = ?, email = ?, senha = ? WHERE id = ?
            """, (nome, cpf, email, senha, id))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def deletar_usuario(id: int):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM usuarios WHERE id = ?", (id,))
            conn.commit()
        finally:
            conn.close()
