from flask import Flask, request
from datetime import datetime
import logging
import requests
from werkzeug.serving import WSGIRequestHandler

# Módulos
from registrar_entrada import registrar_entrada
from registrar_gasto import registrar_gasto
# from registrar_cartao import registrar_cartao
from consultar_gastos import consultar_gastos

# =====================================================
# CONFIGURAÇÃO
# =====================================================
app = Flask(__name__)

NOME_BOT = "Bot Financeiro"
VERSAO = "1.0.0"

HOST = "0.0.0.0"
PORTA = 5000
DEBUG = True

# WhatsApp
GRUPO_FINANCEIRO = "120363427144812522@g.us"

# Evolution API
URL_EVOLUTION = "http://localhost:8080/message/sendText/Financeiro"
APIKEY = "financeiro-casal-teto-para-dois-2026"

# =====================================================
# FUNÇÕES AUXILIARES
# =====================================================
def resposta_robo(texto: str) -> str:
    return f"🤖 *ROBO:*\n\n{texto}"


def enviar_mensagem(texto: str) -> bool:
    headers = {
        "apikey": APIKEY,
        "Content-Type": "application/json",
    }
    payload = {
        "number": GRUPO_FINANCEIRO,
        "text": resposta_robo(texto),
    }
    try:
        resposta = requests.post(
            URL_EVOLUTION, json=payload, headers=headers, timeout=10
        )
        resposta.raise_for_status()
        return True
    except requests.RequestException as erro:
        print(f"\n❌ Erro ao enviar mensagem: {erro}")
        return False


def eh_mensagem_do_robo(texto: str) -> bool:
    if not texto:
        return False
    texto = texto.lower().strip()
    prefixos = ("🤖", "robo:", "*robo*", "bot:", "assistant:")
    return any(texto.startswith(p) for p in prefixos)


def responder(funcao, *args):
    try:
        resposta = funcao(*args)
        if resposta:
            enviar_mensagem(resposta)
    except Exception as erro:
        print(f"\n❌ Erro ao executar {funcao.__name__}: {erro}")
        enviar_mensagem(f"❌ Erro: {str(erro)[:200]}")


def converter_data(data_msg: str) -> datetime:
    try:
        return datetime.fromisoformat(data_msg.replace("Z", "+00:00"))
    except (AttributeError, ValueError, TypeError):
        return datetime.now()


def log_comando(comando: str, pessoa: str, key: dict):
    print("\n" + "=" * 60)
    print(f"👤 Pessoa : {pessoa}")
    print(f"💬 Comando : {comando}")
    print(f"🆔 ID     : {key.get('id')}")
    print("=" * 60)


# =====================================================
# WEBHOOK
# =====================================================
@app.route("/webhook", methods=["POST"])
def webhook():
    dados = request.json
    if not dados or dados.get("event") != "messages.upsert":
        return "OK"

    data = dados.get("data", {})
    key = data.get("key", {})
    message = data.get("message", {})

    if "senderKeyDistributionMessage" in message:
        return "OK"

    if key.get("remoteJid") != GRUPO_FINANCEIRO:
        return "OK"

    mensagem_raw = message.get("conversation")
    if not mensagem_raw:
        return "OK"

    mensagem_raw = mensagem_raw.strip()
    if eh_mensagem_do_robo(mensagem_raw):
        return "OK"

    mensagem = mensagem_raw.lower()
    pessoa = data.get("pushName", "Desconhecido")
    data_convertida = converter_data(dados.get("date_time", ""))

    log_comando(mensagem_raw, pessoa, key)

    # ====================== COMANDOS ======================
    if mensagem in ("teste", "ping"):
        enviar_mensagem("✅ Sistema funcionando corretamente!")
        return "OK"

    elif mensagem in ("help", "ajuda"):
        enviar_mensagem(
            "*Comandos disponíveis:*\n\n"
            "🧪 `teste`\n"
            "💰 `entrada`\n"
            "💸 `gasto`\n"
            "📌 `divida`\n"
            "📊 `extrato`\n\n"
            "Digite `help <comando>` para mais detalhes."
        )
        return "OK"

    # Help específico
    elif mensagem.startswith(("help ", "ajuda ")):
        comando = mensagem.split(maxsplit=1)[1]
        if "entrada" in comando:
            enviar_mensagem(
                "💰 *ENTRADA*\n\n"
                "*Formato:*\n`entrada <origem> <valor> [descrição]`\n\n"
                "*Exemplos:*\n"
                "• `entrada salario 3500`\n"
                "• `entrada pix 250 João`\n"
                "• `entrada venda 900 Notebook`"
            )
        elif "gasto" in comando:
            enviar_mensagem(
                "💸 *GASTO*\n\n"
                "*Formato:*\n`gasto <forma> <descrição> <valor>`\n\n"
                "*Exemplos:*\n"
                "• `gasto pix mercado 152`\n"
                "• `gasto credito amazon 350`"
            )
        elif "divida" in comando or "dívida" in comando:
            enviar_mensagem(
                "📌 *DÍVIDA*\n\n"
                "*Formato:*\n`divida <descrição> <valor>`"
            )
        elif "extrato" in comando:
            enviar_mensagem(
                "📊 *EXTRATO*\n\n"
                "• `extrato` → mês atual\n"
                "• `extrato anterior` → mês passado"
            )
        else:
            enviar_mensagem("❓ Comando não encontrado.")
        return "OK"

    # ==================== COMANDOS PRINCIPAIS ====================
    elif mensagem.startswith("gasto"):
        responder(registrar_gasto, mensagem_raw, pessoa, data_convertida)
        return "OK"

    elif mensagem.startswith("entrada"):
        responder(registrar_entrada, mensagem_raw, pessoa, data_convertida)
        return "OK"

    elif mensagem.startswith("extrato"):
        try:
            mes = data_convertida.month
            ano = data_convertida.year
            if "anterior" in mensagem:
                mes -= 1
                if mes == 0:
                    mes = 12
                    ano -= 1
            relatorio = consultar_gastos(mes, ano)
            enviar_mensagem(relatorio)
        except Exception as e:
            enviar_mensagem("❌ Não foi possível gerar o extrato.")
            print(f"Erro extrato: {e}")
        return "OK"

    # Comando desconhecido
    else:
        enviar_mensagem(
            "❓ *Comando não reconhecido.*\n\n"
            "Digite *help* para ver os comandos disponíveis."
        )
        return "OK"


# =====================================================
if __name__ == "__main__":
    WSGIRequestHandler.log_request = lambda *args, **kwargs: None
    logging.getLogger("werkzeug").setLevel(logging.ERROR)

    print("=" * 60)
    print(f"🤖 {NOME_BOT} v{VERSAO}")
    print(f"Grupo : {GRUPO_FINANCEIRO}")
    print(f"Host  : {HOST}:{PORTA}")
    print("=" * 60)
    print("✅ Aguardando mensagens...\n")

    app.run(host=HOST, port=PORTA, debug=DEBUG, use_reloader=False)