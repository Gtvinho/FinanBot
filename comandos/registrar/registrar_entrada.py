from database import get_connection


def ajustar_valor(valor):
    valor = float(valor)
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def registrar_entrada(mensagem_completa, pessoa, data):
    if len((mensagem_completa.split())) < 3: 
        return "❌ Formato inválido.\nUse: entrada <cartao> <valor> [descrição]"

    """
    Formato:
    entrada <cartao> <valor> [descrição]

    Exemplos:
    entrada salario 3500
    entrada pix 250 João
    entrada venda 800 Notebook
    """

    mensagem = mensagem_completa.split()

    if len(mensagem) < 3:
        raise ValueError(
            "❌ Formato inválido.\n\n"
            "Use:\n"
            "entrada <origem> <valor> [descrição]"
        )

    origem = mensagem[1].lower()

    try:
        valor = float(mensagem[2].replace(",", "."))
    except ValueError:
        raise ValueError("❌ Valor inválido.")

    if valor <= 0:
        raise ValueError("❌ O valor deve ser maior que zero.")

    descricao = " ".join(mensagem[3:]).strip()

    if not descricao:
        descricao = "Entrada"

    # Categoria automática (pode ser alterada futuramente)
    categorias = {
        "salario": "Salário",
        "vale": "Vale",
        "pix": "Transferência",
        "transferencia": "Transferência",
        "venda": "Venda"
    }

    categoria = categorias.get(origem, "Outros")

    data_formatada = data.date()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO entradas (
            pessoa,
            origem,
            descricao,
            categoria,
            valor,
            data,
            observacao
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        pessoa,
        origem,
        descricao,
        categoria,
        valor,
        data_formatada,
        None
    ))

    conn.commit()
    conn.close()

    return (
        "✅ *Entrada registrada!*\n\n"
        f"👤 Pessoa: {pessoa}\n"
        f"📥 Origem: {origem.title()}\n"
        f"🏷️ Categoria: {categoria}\n"
        f"💰 Valor: R$ {ajustar_valor(valor)}\n"
        f"📝 Descrição: {descricao}\n"
        f"📅 Data: {data_formatada}"
    )