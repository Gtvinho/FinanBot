from database import get_connection


def ajustar_valor(valor):
    return f"{float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def consultar_gastos(mes, ano):
    conn = get_connection()
    cursor = conn.cursor()

    data_inicio = f"{ano}-{mes:02d}-01"

    if mes == 12:
        data_fim = f"{ano + 1}-01-01"
    else:
        data_fim = f"{ano}-{mes + 1:02d}-01"

    # ============================
    # ENTRADAS
    # ============================

    cursor.execute("""
        SELECT
            data,
            pessoa,
            origem,
            categoria,
            descricao,
            valor
        FROM entradas
        WHERE data >= ? AND data < ?
        ORDER BY data
    """, (data_inicio, data_fim))

    entradas = cursor.fetchall()

    # ============================
    # GASTOS
    # ============================

    cursor.execute("""
        SELECT
            data,
            pessoa,
            descricao,
            categoria,
            forma_pagamento,
            valor
        FROM gastos
        WHERE data >= ? AND data < ?
        ORDER BY data
    """, (data_inicio, data_fim))

    gastos = cursor.fetchall()

    # ============================
    # DÍVIDAS
    # ============================

    cursor.execute("""
        SELECT
            descricao,
            valor,
            status
        FROM dividas
        WHERE status = 'aberta'
        ORDER BY data
    """)

    dividas = cursor.fetchall()

    conn.close()

    total_entradas = sum(item["valor"] for item in entradas)
    total_gastos = sum(item["valor"] for item in gastos)
    total_dividas = sum(item["valor"] for item in dividas)

    saldo = total_entradas - total_gastos

    relatorio = []
    relatorio.append(f"📊 *EXTRATO {mes:02d}/{ano}*")
    relatorio.append("")

    # ============================
    # ENTRADAS
    # ============================

    relatorio.append("📥 *ENTRADAS*")

    if entradas:

        for e in entradas:
            relatorio.append(
                f"• {e['data']} | {e['origem'].title()} | "
                f"R$ {ajustar_valor(e['valor'])}"
            )

            if e["descricao"]:
                relatorio.append(f"  {e['descricao']}")

        relatorio.append("")
        relatorio.append(f"Total: R$ {ajustar_valor(total_entradas)}")

    else:
        relatorio.append("Nenhuma entrada.")

    relatorio.append("")
    relatorio.append("────────────────────")

    # ============================
    # GASTOS
    # ============================

    relatorio.append("💸 *GASTOS*")

    if gastos:

        for g in gastos:
            relatorio.append(
                f"• {g['data']} | {g['descricao']}"
            )
            relatorio.append(
                f"  {g['forma_pagamento'].title()} | "
                f"R$ {ajustar_valor(g['valor'])}"
            )

        relatorio.append("")
        relatorio.append(f"Total: R$ {ajustar_valor(total_gastos)}")

    else:
        relatorio.append("Nenhum gasto.")

    relatorio.append("")
    relatorio.append("────────────────────")

    # ============================
    # DÍVIDAS
    # ============================

    relatorio.append("📌 *DÍVIDAS*")

    if dividas:

        for d in dividas:
            relatorio.append(
                f"• {d['descricao']} - R$ {ajustar_valor(d['valor'])}"
            )

        relatorio.append("")
        relatorio.append(f"Total: R$ {ajustar_valor(total_dividas)}")

    else:
        relatorio.append("Nenhuma dívida.")

    relatorio.append("")
    relatorio.append("────────────────────")

    relatorio.append(
        f"💰 *Saldo:* R$ {ajustar_valor(saldo)}"
    )

    return "\n".join(relatorio)