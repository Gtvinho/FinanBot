def enviar_mensagem_help_entrada():
    texto = (
        "💰 *ENTRADA*\n\n"
        "*Formato:*\n`entrada <banco> <valor> [descrição]`\n\n"
        "*Exemplos:*\n"
        "• `entrada salario 3500`\n"
        "• `entrada pix 250 João`\n"
        "• `entrada venda 900 Notebook`"
    )
    return texto

##########################################################################
def enviar_mensagem_help_gasto():
    texto = (
        "💸 *GASTO*\n\n"
        "*Formato:*\n`gasto <forma> <descrição> <valor>`\n\n"
        "*Exemplos:*\n"
        "• `gasto pix mercado 152`\n"
        "• `gasto credito amazon 350`"
    )
    return texto

##########################################################################
def enviar_mensagem_help_divida():
    texto = (
        "📌 *DÍVIDA*\n\n"
        "*Formato:*\n`divida <descrição> <valor>`"
    )
    return texto

##########################################################################
def enviar_mensagem_help_extrato():
    texto =(
        "📊 *EXTRATO*\n\n"
        "• `extrato` → mês atual\n"
        "• `extrato anterior` → mês passado"
    )
    return texto

##########################################################################
def enviar_mensagem_help_parcelas():
    texto =(
        "💳 *CRÉDITO PARCELADO*\n\n"
        "Registra uma compra parcelada no cartão de crédito.\n\n"
        "*Formato:*\n"
        "`credito_parcelado <descrição> <valor_total> <parcelas>`\n\n"
        "*Exemplos:*\n"
        "• `credito_parcelado notebook 4500 12`\n"
        "• `credito_parcelado iphone 7200 24`\n"
        "• `credito_parcelado sofa 2800 10`\n"
        "• `credito_parcelado passagem sp 1350 6`\n\n"
        "✅ O sistema calcula automaticamente o valor de cada parcela.\n"
        "📊 No extrato aparecerá apenas a parcela do mês atual."
        )
    return texto

##########################################################################