from datetime import datetime
from database import get_connection

class Transferencia:
    @staticmethod
    def realizar_transferencia(conta_origem_id: int, conta_destino_id: int, valor: float):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT saldo FROM contas WHERE id = ?", (conta_origem_id,))
            saldo_origem = cursor.fetchone()
            cursor.execute("SELECT saldo FROM contas WHERE id = ?", (conta_destino_id,))
            saldo_destino = cursor.fetchone()

            if saldo_origem is None or saldo_destino is None:
                raise ValueError("Uma das contas não existe.")

            saldo_origem = saldo_origem[0]
            if saldo_origem < valor:
                raise ValueError("Saldo insuficiente para a transferência.")

            novo_saldo_origem = saldo_origem - valor
            cursor.execute("UPDATE contas SET saldo = ? WHERE id = ?", (novo_saldo_origem, conta_origem_id))

            saldo_destino = saldo_destino[0]
            novo_saldo_destino = saldo_destino + valor
            cursor.execute("UPDATE contas SET saldo = ? WHERE id = ?", (novo_saldo_destino, conta_destino_id))

            data = datetime.now().isoformat()
            cursor.execute("""
            INSERT INTO transferencias (conta_origem_id, conta_destino_id, valor, data)
            VALUES (?, ?, ?, ?)
            """, (conta_origem_id, conta_destino_id, valor, data))

            conn.commit()
        finally:
            conn.close()
    
    @staticmethod
    def listar_transferencias(conta_origem_id: int = None, conta_destino_id: int = None):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            query = "SELECT * FROM transferencias WHERE 1=1"
            params = []

            if conta_origem_id is not None:
                query += " AND conta_origem_id = ?"
                params.append(conta_origem_id)
            
            if conta_destino_id is not None:
                query += " AND conta_destino_id = ?"
                params.append(conta_destino_id)
            
            cursor.execute(query, params)
            transferencias = cursor.fetchall()
            
            result = []
            for transferencia in transferencias:
                result.append({
                    "id": transferencia[0],
                    "conta_origem_id": transferencia[1],
                    "conta_destino_id": transferencia[2],
                    "valor": transferencia[3],
                    "data": transferencia[4]
                })
            
            return result
        finally:
            conn.close()