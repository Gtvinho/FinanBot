
def buscar_cliente_por_jid(jid: str):
    """Retorna os dados do cliente pelo JID (número WhatsApp)"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nome, status, plano, validade 
        FROM clientes 
        WHERE telefone = ? 
        LIMIT 1
    """, (jid,))
    return cursor.fetchone()