from database import get_connection

def ajustar_valor(valor):
    return f"{float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def consultar_gastos(mes: int, ano: int):
    conn = get_connection()
    cursor = conn.cursor()
    
    data_inicio = f"{ano}-{mes:02d}-01"
    data_fim = f"{ano + 1 if mes == 12 else ano}-{1 if mes == 12 else mes + 1:02d}-01"

    cursor.execute("SELECT data, pessoa, origem, categoria, descricao, valor FROM entradas WHERE data >= ? AND data < ? ORDER BY data", (data_inicio, data_fim))
    entradas = cursor.fetchall()

    cursor.execute("SELECT data, pessoa, descricao, categoria, forma_pagamento, valor FROM gastos WHERE data >= ? AND data < ? ORDER BY data", (data_inicio, data_fim))
    gastos = cursor.fetchall()

    cursor.execute("SELECT data, tipo, descricao, valor FROM vales WHERE data >= ? AND data < ? ORDER BY data", (data_inicio, data_fim))
    vales = cursor.fetchall()

    cursor.execute("SELECT descricao, valor_parcela, parcela_atual, num_parcelas, mes_inicio, ano_inicio FROM creditos_parcelados")
    todos_parcelados = cursor.fetchall()

    parcelas_pagas = []
    parcelas_novas = []
    for p in todos_parcelados:
        mes_inicio = p['mes_inicio']
        ano_inicio = p['ano_inicio']
        if mes_inicio is None or ano_inicio is None:
            parcelas_novas.append(p)
            continue
        if (ano_inicio < ano) or (ano_inicio == ano and mes_inicio < mes):
            parcelas_pagas.append(p)
        elif ano_inicio == ano and mes_inicio == mes:
            parcelas_novas.append(p)

    cursor.execute("SELECT descricao, valor, status FROM dividas WHERE status = 'aberta'")
    dividas = cursor.fetchall()

    conn.close()

    # ============================
    # CÁLCULOS
    # ============================
    total_entradas = sum(item["valor"] for item in entradas)
    total_gastos_normais = 0
    total_gastos_vale = 0

    for g in gastos:
        if g['forma_pagamento'].lower() == 'vale' or 'vale' in g['descricao'].lower():
            total_gastos_vale += g["valor"]
        else:
            total_gastos_normais += g["valor"]

    total_vales = sum(item["valor"] for item in vales)
    total_parcelados_desconto = sum(item["valor_parcela"] for item in parcelas_pagas)
    total_dividas = sum(item["valor"] for item in dividas)

    saldo = total_entradas - total_gastos_normais - total_parcelados_desconto
    saldo_vale = total_vales - total_gastos_vale
    # ============================
    # RELATÓRIO
    # ============================
    relatorio = [f"📊 *EXTRATO {mes:02d}/{ano}*\n"]

    relatorio.append("📥 *ENTRADAS*")
    if entradas:
        for e in entradas:
            desc = f" - {e['descricao']}" if e['descricao'] else ""
            relatorio.append(f"• {e['data'][:10]} | {e['origem'].title()} | R$ {ajustar_valor(e['valor'])}{desc}")
        relatorio.append(f"**Total Entradas:** R$ {ajustar_valor(total_entradas)}")
    else:
        relatorio.append("Nenhuma entrada.")

    relatorio.append("\n🎟️ *VALES*")
    if vales or total_gastos_vale > 0:
        for v in vales:
            desc = f" - {v['descricao']}" if v['descricao'] else ""
            relatorio.append(f"• {v['data'][:10]} | {v['tipo'].title()} | R$ {ajustar_valor(v['valor'])}{desc}")
        if total_gastos_vale > 0:
            relatorio.append(f"**Gastos com Vale:** - R$ {ajustar_valor(total_gastos_vale)}")
        relatorio.append(f"**Saldo Vale:** R$ {ajustar_valor(saldo_vale)}")
    else:
        relatorio.append("Nenhum vale este mês.")

    relatorio.append("\n💸 *GASTOS*")
    if gastos:
        for g in gastos:
            if g['forma_pagamento'].lower() == 'vale' or 'vale' in g['descricao'].lower():
                relatorio.append(f"• {g['data'][:10]} | {g['descricao']} (Vale)")
            else:
                relatorio.append(f"• {g['data'][:10]} | {g['descricao']}")
            relatorio.append(f"  {g['forma_pagamento'].title()} | R$ {ajustar_valor(g['valor'])}")
        relatorio.append(f"**Total Gastos Normais:** R$ {ajustar_valor(total_gastos_normais)}")
    else:
        relatorio.append("Nenhum gasto.")
    relatorio.append("\n💳 *PARCELADOS*")
    relatorio.append(" ✅ *Parcelas Pagas*")
    if parcelas_pagas:
        for p in parcelas_pagas:
            relatorio.append(f" • {p['descricao']} ({p['parcela_atual']}/{p['num_parcelas']}) R$ {ajustar_valor(p['valor_parcela'])}")
        relatorio.append(f" **Total Pago:** R$ {ajustar_valor(sum(p['valor_parcela'] for p in parcelas_pagas))}")
    else:
        relatorio.append(" Nenhuma")

    relatorio.append("\n ⏳ *Parcelas deste mês*")
    if parcelas_novas:
        for p in parcelas_novas:
            relatorio.append(f" • {p['descricao']} ({p['parcela_atual']}/{p['num_parcelas']}) R$ {ajustar_valor(p['valor_parcela'])}")
        relatorio.append(f" **Total a Pagar:** R$ {ajustar_valor(sum(p['valor_parcela'] for p in parcelas_novas))}")
    else:
        relatorio.append(" Nenhuma")

    relatorio.append("\n📌 *DÍVIDAS EM ABERTO*")
    if dividas:
        for d in dividas:
            relatorio.append(f"• {d['descricao']} - R$ {ajustar_valor(d['valor'])}")
        relatorio.append(f"**Total Dívidas:** R$ {ajustar_valor(total_dividas)}")
    else:
        relatorio.append("Nenhuma dívida.")

    relatorio.append(f"\n💰 *SALDO DO MÊS:* R$ {ajustar_valor(saldo)}")
    if 'saldo_vale' in locals():
        relatorio.append(f"🎟️ *Saldo Vale:* R$ {ajustar_valor(saldo_vale)}")

    return "\n".join(relatorio)