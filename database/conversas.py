# database/conversas.py
from .db import get_connection


def buscar_cliente_por_jid(jid):
    """Busca cliente ativo pelo JID do WhatsApp."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT c.*
            FROM conversas conv
            JOIN clientes c
                ON c.id = conv.cliente_id
            WHERE conv.jid = ?
              AND conv.ativo = 1
        """, (jid,))
        
        cliente = cursor.fetchone()
        return cliente
        
    except Exception as e:
        print(f"❌ Erro ao buscar cliente por JID: {e}")
        return None
    finally:
        conn.close()