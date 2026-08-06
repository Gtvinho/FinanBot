# database/conversas.py
from database.adm_server_banco.db import get_connection
    
def ativar_por_codigo(jid: str, codigo: str):
    """Ativa o cliente usando o código"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id FROM clientes WHERE codigo_ativacao = ?", (codigo.upper(),))
        cliente = cursor.fetchone()
        
        if not cliente:
            return "❌ Código de ativação inválido."
        
        cursor.execute("""
            UPDATE clientes 
            SET telefone = ?, status = 'Ativo' 
            WHERE id = ?
        """, (jid, cliente['id']))
        
        conn.commit()
        return "✅ Ativação realizada com sucesso!\nBem-vindo ao Financeiro Bot!"
    except Exception as e:
        print(e)
        return "❌ Erro ao ativar o bot."
    finally:
        conn.close()