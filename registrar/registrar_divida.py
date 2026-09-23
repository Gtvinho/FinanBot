from database import get_connection


def ajustar_valor(valor):
    valor = float(valor)
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def registrar_divida(mensagem_completa, pessoa, data):
    """
    Registra uma dívida.

    Formato:
        divida <descrição> <valor>

    Exemplos:
        divida oficina 1200
        divida joao 300
        divida aluguel 1500
    """

    partes = mensagem_completa.split()

    if len(partes) < 3:
        raise ValueError(
            "❌ Formato inválido.\n\n"
            "Use:\n"
            "divida <descrição> <valor>\n\n"
            "Exemplos:\n"
            "divida oficina 1200\n"
            "divida joao 300"
        )

    try:
        valor = float(partes[-1].replace(",", "."))
    except ValueError:
        raise ValueError("❌ Valor inválido.")

    if valor <= 0:
        raise ValueError("❌ O valor deve ser maior que zero.")

    descricao = " ".join(partes[1:-1]).strip()

    if not descricao:
        raise ValueError("❌ Informe uma descrição para a dívida.")

    categoria = "Outros"
    observacao = None
    status = "aberta"

    data_formatada = data.date()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO dividas (
            pessoa,
            descricao,
            categoria,
            valor,
            status,
            data,
            observacao
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        pessoa,
        descricao,
        categoria,
        valor,
        status,
        data_formatada,
        observacao
    ))

    conn.commit()
    conn.close()

    return (
        "✅ *Dívida registrada!*\n\n"
        f"👤 Pessoa: {pessoa}\n"
        f"📝 Descrição: {descricao}\n"
        f"💰 Valor: R$ {ajustar_valor(valor)}\n"
        f"📌 Status: {status.capitalize()}\n"
        f"📅 Data: {data_formatada}"
    )