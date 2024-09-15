from database import get_connection

class ContaBancaria:
    def __init__(self, usuario_id: int, saldo: float, tipo: str):
        self.__usuario_id = usuario_id
        self.__saldo = saldo
        self.__tipo = tipo

    def get_usuario_id(self) -> int:
        return self.__usuario_id

    def get_saldo(self) -> float:
        return self.__saldo

    def get_tipo(self) -> str:
        return self.__tipo

    def set_saldo(self, saldo: float):
        self.__saldo = saldo

    def set_tipo(self, tipo: str):
        self.__tipo = tipo


    @staticmethod
    def criar_conta(usuario_id: int, saldo: float, tipo: int):
        if tipo not in (1,2):
            raise ValueError("Tipo de conta deve ser 1 (corrente) ou 2 (poupança).")

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
            INSERT INTO contas (usuario_id, saldo, tipo)
            VALUES (?, ?, ?)
            """, (usuario_id, saldo, tipo))

            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def buscar_conta(id: int):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM contas WHERE id = ?", (id,))
            conta = cursor.fetchone()
            if conta:
                return {
                    "id": conta[0],
                    "usuario_id": conta[1],
                    "saldo": conta[2],
                    "tipo": conta[3]
                }
            else:
                return None
        finally:
            conn.close()

    @staticmethod
    def atualizar_conta(id: int, saldo: float, tipo: str):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE contas SET saldo = ?, tipo = ? WHERE id = ?
            """, (saldo, tipo, id))
            conn.commit()
        finally:
            conn.close()


    @staticmethod
    def encerrar_conta(id: int):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT saldo FROM contas WHERE usuario_id = ?", (id,))
            saldo = cursor.fetchone()
            
            if saldo is None:
                raise ValueError("Conta não encontrada.")

            if saldo[0] > 0.0:
                raise ValueError("A conta não pode ser encerrada enquanto tiver saldo.")
            
            cursor.execute("DELETE FROM contas WHERE usuario_id = ?", (id,))
            conn.commit()
        finally:
            conn.close()
