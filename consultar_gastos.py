from database import get_connection

def ajustar_valor(valor):
    """Formata valor no padrão brasileiro"""
    return f"{float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def consultar_gastos(mes: int, ano: int):
    conn = get_connection()
    cursor = conn.cursor()
    
    data_inicio = f"{ano}-{mes:02d}-01"
    data_fim = f"{ano + 1 if mes == 12 else ano}-{1 if mes == 12 else mes + 1:02d}-01"

    # ============================
    # ENTRADAS
    # ============================
    cursor.execute("""
        SELECT data, pessoa, origem, categoria, descricao, valor
        FROM entradas
        WHERE data >= ? AND data < ?
        ORDER BY data
    """, (data_inicio, data_fim))
    entradas = cursor.fetchall()

    # ============================
    # GASTOS
    # ============================
    cursor.execute("""
        SELECT data, pessoa, descricao, categoria, forma_pagamento, valor
        FROM gastos
        WHERE data >= ? AND data < ?
        ORDER BY data
    """, (data_inicio, data_fim))
    gastos = cursor.fetchall()

    # ============================
    # VALES
    # ============================
    cursor.execute("""
        SELECT data, tipo, descricao, valor
        FROM vales
        WHERE data >= ? AND data < ?
        ORDER BY data
    """, (data_inicio, data_fim))
    vales = cursor.fetchall()

    # ============================
    # CRÉDITO PARCELADO
    # ============================
    cursor.execute("""
        SELECT descricao, valor_parcela, parcela_atual, num_parcelas
        FROM creditos_parcelados 
        WHERE (CAST(strftime('%Y', data_compra) AS INTEGER) * 12 + 
               CAST(strftime('%m', data_compra) AS INTEGER) + parcela_atual - 1) 
              = (? * 12 + ?)
    """, (ano, mes))
    parcelados = cursor.fetchall()

    # ============================
    # DÍVIDAS
    # ============================
    cursor.execute("""
        SELECT descricao, valor, status
        FROM dividas
        WHERE status = 'aberta'
    """)
    dividas = cursor.fetchall()

    conn.close()

    # Cálculos
    total_entradas = sum(item["valor"] for item in entradas)
    total_gastos = sum(item["valor"] for item in gastos)
    total_vales = sum(item["valor"] for item in vales)
    total_parcelados = sum(item["valor_parcela"] for item in parcelados)
    total_dividas = sum(item["valor"] for item in dividas)

    saldo = total_entradas - total_gastos - total_parcelados

    # ============================
    # MONTAGEM DO RELATÓRIO
    # ============================
    relatorio = [f"📊 *EXTRATO {mes:02d}/{ano}*\n"]

    # Entradas
    relatorio.append("📥 *ENTRADAS*")
    if entradas:
        for e in entradas:
            descricao = f" - {e['descricao']}" if e['descricao'] else ""
            relatorio.append(
                f"• {e['data'][:10]} | {e['origem'].title()} | R$ {ajustar_valor(e['valor'])}{descricao}"
            )
        relatorio.append(f"**Total Entradas:** R$ {ajustar_valor(total_entradas)}")
    else:
        relatorio.append("Nenhuma entrada.")
    relatorio.append("\n────────────────────")

    # Vales
    relatorio.append("🎟️ *VALES*")
    if vales:
        for v in vales:
            descricao = f" - {v['descricao']}" if v['descricao'] else ""
            relatorio.append(
                f"• {v['data'][:10]} | {v['tipo'].title()} | R$ {ajustar_valor(v['valor'])}{descricao}"
            )
        relatorio.append(f"**Total Vales:** R$ {ajustar_valor(total_vales)}")
    else:
        relatorio.append("Nenhum vale este mês.")
    relatorio.append("\n────────────────────")

    # Gastos
    relatorio.append("💸 *GASTOS*")
    if gastos:
        for g in gastos:
            relatorio.append(f"• {g['data'][:10]} | {g['descricao']}")
            relatorio.append(f"  {g['forma_pagamento'].title()} | R$ {ajustar_valor(g['valor'])}")
        relatorio.append(f"**Total Gastos:** R$ {ajustar_valor(total_gastos)}")
    else:
        relatorio.append("Nenhum gasto.")
    relatorio.append("\n────────────────────")

    # Parcelados
    relatorio.append("💳 *PARCELADOS*")
    if parcelados:
        for p in parcelados:
            relatorio.append(
                f"• {p['descricao']} ({p['parcela_atual']}/{p['num_parcelas']}) "
                f"R$ {ajustar_valor(p['valor_parcela'])}"
            )
        relatorio.append(f"**Total Parcelas:** R$ {ajustar_valor(total_parcelados)}")
    else:
        relatorio.append("Nenhuma parcela este mês.")
    relatorio.append("\n────────────────────")

    # Dívidas
    relatorio.append("📌 *DÍVIDAS EM ABERTO*")
    if dividas:
        for d in dividas:
            relatorio.append(f"• {d['descricao']} - R$ {ajustar_valor(d['valor'])}")
        relatorio.append(f"**Total Dívidas:** R$ {ajustar_valor(total_dividas)}")
    else:
        relatorio.append("Nenhuma dívida em aberto.")

    relatorio.append(f"\n💰 *SALDO DO MÊS:* R$ {ajustar_valor(saldo)}")

    return "\n".join(relatorio)