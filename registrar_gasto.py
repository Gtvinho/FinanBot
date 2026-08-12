from database import get_connection


def ajustar_valor(valor):
    valor = float(valor)
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def registrar_gasto(mensagem_completa, pessoa, data):
    """
    Formato:
    gasto <forma_pagamento> <descrição> <valor>

    Exemplos:
    gasto pix mercado 150
    gasto debito gasolina 80
    gasto dinheiro lanche 25
    """

    partes = mensagem_completa.split()

    if len(partes) < 4:
        raise ValueError(
            "❌ Formato inválido.\n\n"
            "Use:\n"
            "gasto <forma_pagamento> <descrição> <valor>"
        )

    forma_pagamento = partes[1].lower()

    formas_validas = [
        "pix",
        "dinheiro",
        "debito",
        "credito",
        "fatura",
        "vale"
    ]

    if forma_pagamento not in formas_validas:
        raise ValueError(
            "❌ Forma de pagamento inválida.\n\n"
            "Use: pix, dinheiro, debito, credito ou fatura."
        )

    try:
        valor = float(partes[-1].replace(",", "."))
    except ValueError:
        raise ValueError("❌ Valor inválido.")

    if valor <= 0:
        raise ValueError("❌ O valor deve ser maior que zero.")

    descricao = " ".join(partes[2:-1]).strip()

    if not descricao:
        descricao = "Gasto"

    # Categoria automática (pode ser alterada depois)
    categoria = "Outros"

    data_formatada = data.date()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO gastos (
            data,
            pessoa,
            descricao,
            categoria,
            forma_pagamento,
            valor,
            observacao
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data_formatada,
        pessoa,
        descricao,
        categoria,
        forma_pagamento,
        valor,
        None
    ))

    conn.commit()
    conn.close()

    return (
        "✅ *Gasto registrado!*\n\n"
        f"👤 Pessoa: {pessoa}\n"
        f"📝 Descrição: {descricao}\n"
        f"💳 Pagamento: {forma_pagamento.title()}\n"
        f"🏷️ Categoria: {categoria}\n"
        f"💰 Valor: R$ {ajustar_valor(valor)}\n"
        f"📅 Data: {data_formatada}"
    )