from database import get_connection

def ajustar_valor(valor):
    return f"{float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def consultar_gastos(mes: int, ano: int):
    conn = get_connection() 
    cursor = conn.cursor()
    
    data_inicio = f"{ano}-{mes:02d}-01"
    data_fim = f"{ano + 1 if mes == 12 else ano}-{1 if mes == 12 else mes + 1:02d}-01"

    # ====================== CONSULTAS ======================
    cursor.execute("SELECT data, pessoa, origem, categoria, descricao, valor FROM entradas WHERE data >= ? AND data < ? ORDER BY data", (data_inicio, data_fim))
    entradas = cursor.fetchall()

    cursor.execute("SELECT data, pessoa, descricao, categoria, forma_pagamento, valor FROM gastos WHERE data >= ? AND data < ? ORDER BY data", (data_inicio, data_fim))
    gastos = cursor.fetchall()

    cursor.execute("SELECT data, tipo, descricao, valor FROM vales WHERE data >= ? AND data < ? ORDER BY data", (data_inicio, data_fim))
    vales = cursor.fetchall()

    cursor.execute("""
        SELECT descricao, valor_parcela, parcela_atual, num_parcelas, 
        mes_inicio, ano_inicio 
        FROM creditos_parcelados 
        WHERE parcela_atual <= num_parcelas 
        ORDER BY ano_inicio, mes_inicio
    """)
    parcelados = cursor.fetchall()

    cursor.execute("SELECT descricao, valor, status FROM dividas WHERE status = 'aberta'")
    dividas = cursor.fetchall()

    conn.close()

    # ====================== CÁLCULOS ======================
    total_entradas = sum(float(item[5]) for item in entradas)
    
    total_gastos_normais = 0.0
    total_gastos_vale = 0.0
    for g in gastos:
        valor = float(g[5])
        if (g[4] and g[4].lower() == 'vale') or 'vale' in str(g[2]).lower():
            total_gastos_vale += valor
        else:
            total_gastos_normais += valor

    total_vales = sum(float(item[3]) for item in vales)
    total_dividas = sum(float(item[1]) for item in dividas)

    # ====================== LÓGICA DE PARCELAS (REGRA ATUALIZADA) ======================
    total_parcelados_desconto = 0.0   # Apenas o que realmente deve descontar este mês
    parcelas_novas = []

    for p in parcelados:
        descricao, valor_parcela, parcela_atual, num_parcelas, mes_inicio, ano_inicio = p
        if mes_inicio is None or ano_inicio is None:
            continue

        deve_contar_este_mes = True

        # REGRA PRINCIPAL:
        # Se for a o mes de compra, desconta no proximo.
        p["parcela_atual"]
        parcela_atual = (ano - p["ano_inicio"]) * 12 + (mes - p["mes_inicio"]) + 1
        if mes_inicio == mes+1:
            deve_contar_este_mes = False
            #print("print 1")
        if deve_contar_este_mes and ((ano_inicio < ano) or (ano_inicio == ano and mes_inicio <= mes) or (ano_inicio == ano and mes_inicio == mes)):
            total_parcelados_desconto += float(valor_parcela)
            parcelas_novas.append(p)
            #print("print 2")
            
    saldo = total_entradas - total_gastos_normais - total_parcelados_desconto
    saldo_vale = total_vales - total_gastos_vale

    # ====================== RELATÓRIO ======================
    relatorio = [f"📊 *EXTRATO {mes:02d}/{ano}*\n"]
##################################################################
##################################################################

    # Entradas, Vales, Gastos... (mantidos iguais)
    relatorio.append("📥 *ENTRADAS*")
    if entradas:
        for e in entradas:
            desc = f" - {e[4]}" if e[4] else ""
            relatorio.append(f"• {str(e[0])[:10]} | {str(e[2]).title() if e[2] else ''} | R$ {ajustar_valor(e[5])}{desc}")
        relatorio.append(f"**Total Entradas:** R$ {ajustar_valor(total_entradas)}")
    else:
        relatorio.append("Nenhuma entrada.")
##################################################################
##################################################################

    relatorio.append("\n🎟️ *VALES*")
    if vales or total_gastos_vale > 0:
        for v in vales:
            desc = f" - {v[2]}" if v[2] else ""
            relatorio.append(f"• {str(v[0])[:10]} | {str(v[1]).title() if v[1] else ''} | R$ {ajustar_valor(v[3])}{desc}")
        if total_gastos_vale > 0:
            relatorio.append(f"**Gastos com Vale:** - R$ {ajustar_valor(total_gastos_vale)}")
    else:
        relatorio.append("Nenhum vale este mês.")

    relatorio.append("\n💸 *GASTOS*")
    if gastos:
        for g in gastos:
            if (g[4] and g[4].lower() == 'vale') or 'vale' in str(g[2]).lower():
                continue
            relatorio.append(f"• {str(g[0])[:10]} | {g[2]} | {str(g[4]).title() if g[4] else ''} | R$ {ajustar_valor(g[5])}")
        relatorio.append(f"**Total Gastos Normais:** R$ {ajustar_valor(total_gastos_normais)}")
    else:
        relatorio.append("Nenhum gasto.")
##################################################################
##################################################################

    # Parcelamentos Ativos
    relatorio.append("\n💳 *PARCELAMENTOS ATIVOS* \n\n *Iniciados este mês*")
    if parcelados:
        for p in parcelados:
            if p[4] != mes:
                relatorio.append(f"• {p[0]} |Valor: R$ {ajustar_valor(p[1])} | Parcelado em: x{p[3]}")
        relatorio.append(f"\n**Total das Parcelas Ativas:** R$ {ajustar_valor(sum(float(p[1]) for p in parcelados))}")
    else:
        relatorio.append("Nenhum parcelamento ativo.")

    # Parcelas deste mês
    relatorio.append("\n⏳ *Parcelas pagas neste mês*")
    if parcelas_novas:
        for p in parcelas_novas:   
            #for coluna in p.keys():
            #    print(coluna, "=", p[coluna])
            parcela_atual = (ano - p["ano_inicio"]) * 12 + (mes - p["mes_inicio"]) + 1
            relatorio.append(f" • {p[0]} ({parcela_atual}/{p[3]}) R$ {ajustar_valor(p[1])}")
        relatorio.append(f" **Total de fatura pago este mês:** R$ {ajustar_valor(total_parcelados_desconto)}")
    else:
        relatorio.append(" Nenhuma")
##################################################################
##################################################################

    relatorio.append("\n📌 *DÍVIDAS EM ABERTO*")
    if dividas:
        for d in dividas:
            relatorio.append(f"• {d[0]} - R$ {ajustar_valor(d[1])}")
        relatorio.append(f"**Total Dívidas:** R$ {ajustar_valor(total_dividas)}")
    else:
        relatorio.append("Nenhuma dívida.")
##################################################################
##################################################################

    relatorio.append(f"\n💰 *SALDO DO MÊS:* R$ {ajustar_valor(saldo)}")
    relatorio.append(f"🎟️ *Saldo Vale:* R$ {ajustar_valor(saldo_vale)}")

    return "\n".join(relatorio)