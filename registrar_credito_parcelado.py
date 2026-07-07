# registrar_credito_parcelado.py
from db import get_conn
from datetime import datetime

def registrar_credito_parcelado(mensagem: str, pessoa: str, data_msg: datetime) -> str:
    try:
        partes = mensagem.split()
        if len(partes) < 4:
            return "❌ Formato inválido.\nUse: `credito_parcelado <descrição> <valor_total> <parcelas>`"

        valor_total_str = partes[-2].replace(',', '.')
        try:
            valor_total = float(valor_total_str)
            num_parcelas = int(partes[-1])
        except ValueError:
            return "❌ Valor ou número de parcelas inválido."

        if num_parcelas < 1 or num_parcelas > 60:
            return "❌ Número de parcelas deve estar entre 1 e 60."

        descricao = " ".join(partes[1:-2])

        valor_parcela = round(valor_total / num_parcelas, 2)

        conn = get_conn()
        conn.execute("""
            INSERT INTO creditos_parcelados 
            (data_compra, descricao, valor_total, num_parcelas, valor_parcela, registrado_por)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data_msg.isoformat(),
            descricao,
            valor_total,
            num_parcelas,
            valor_parcela,
            pessoa
        ))
        conn.commit()
        conn.close()

        return f"""✅ *Crédito Parcelado registrado!*

📌 {descricao}
💰 Total: R$ {valor_total:,.2f}
📦 {num_parcelas}x de R$ {valor_parcela:,.2f}"""

    except Exception as e:
        return f"❌ Erro ao registrar parcelado: {str(e)}"