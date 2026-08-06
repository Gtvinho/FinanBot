
from database.users_server_banco.db import get_connection

def buscar_cliente_por_jid(jid: str):
    """Retorna os dados do cliente pelo JID (número WhatsApp)"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ID, NOME 
        FROM usuarios 
        WHERE JID = ? 
        LIMIT 1
    """, (jid,))
    return cursor.fetchone()