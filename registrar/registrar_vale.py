# registrar_vale.py
from database import get_connection
from datetime import datetime

def registrar_vale(mensagem: str, pessoa: str, data_msg: datetime) -> str:
    try:
        partes = mensagem.split()
        if len(partes) < 3:
            return "❌ Formato inválido.\nUse: `vale <tipo> <valor> [descrição]`"

        tipo = partes[1].lower()
        try:
            valor = float(partes[2].replace(',', '.'))
        except ValueError:
            return "❌ Valor inválido."

        descricao = " ".join(partes[3:]) if len(partes) > 3 else ""

        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO vales (data, pessoa, tipo, descricao, valor)
            VALUES (?, ?, ?, ?, ?)
        """, (data_msg.isoformat(), pessoa, tipo, descricao, valor))
        
        conn.commit()
        conn.close()

        return f"""✅ *Vale registrado!*

📌 Tipo: {tipo.title()}
💰 Valor: R$ {valor:,.2f}
👤 Por: {pessoa}"""

    except Exception as e:
        return f"❌ Erro ao registrar vale: {str(e)}"