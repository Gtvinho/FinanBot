def enviar_mensagem_help():
    """Retorna a mensagem de ajuda principal do bot."""
    texto = (
        "*📋 Comandos Disponíveis:*\n\n"
        "ℹ️ `sobre` — Informações sobre o bot e sua versao\n"
        "🧪 `teste` / `ping` — Verificar se o bot está online\n"
        "💰 `entrada` — Registrar uma entrada\n"
        "💸 `gasto` — Registrar um gasto\n"
        "📌 `divida` — Registrar uma dívida\n"
        "💳 `credito_parcelado` — Compra parcelada\n"
        "📊 `extrato` — Ver extrato do mês\n\n"
        "Digite `help <comando>` para ver detalhes de um comando específico."
    )
    return texto