from flask import Flask, request
from datetime import datetime
import logging
import requests
from werkzeug.serving import WSGIRequestHandler
from datetime import datetime, timedelta, timezone

# ====================== IMPORTS ======================
from database.adm_server_banco.db import get_connection
from database.users_server_banco.usuarios import buscar_cliente_por_jid

# Comandos
#from comandos.registrar.registrar_entrada import registrar_entrada
#from comandos.registrar.registrar_gasto import registrar_gasto
#from comandos.registrar.registrar_vale import registrar_vale
#from comandos.registrar.registrar_credito import registrar_credito
#from comandos.registrar.registrar_divida import registrar_divida

# Mensagens
from mensagens_automaticas.help import enviar_mensagem_help
from mensagens_automaticas.gerenciador_mensagens import identificar_mensagem_help

# Systema
from systema.verificacao import verificar_dados


# ====================== CONFIGURAÇÃO ======================
app = Flask(__name__)
HOST = "0.0.0.0"
PORTA = 5000
DEBUG = True

# Evolution API
URL_EVOLUTION = "http://localhost:8080/message/sendText/Financeiro"
APIKEY = "financeiro-casal-teto-para-dois-2026"

NOME_BOT = "Financeiro Bot"
VERSAO = "1.2.0"
CRIADOR = "Gustavo Franzen Elicker"
ANO = "2026"


# =====================================================
# FUNÇÕES AUXILIARES
# =====================================================
def resposta_robo(texto: str) -> str:
    return f"🤖 *ROBO EM HOMOLOGACAO :*\n\n{texto}"


def enviar_mensagem(texto: str, numero: str) -> bool:
    headers = {
        "apikey": APIKEY,
        "Content-Type": "application/json",
    }
    payload = {
        "number": numero,
        "text": resposta_robo(texto),
    }
    try:
        resposta = requests.post(URL_EVOLUTION, json=payload, headers=headers, timeout=10)
        resposta.raise_for_status()
        return True
    except requests.RequestException as erro:
        print(f"\n❌ Erro ao enviar mensagem: {erro}")
        return False


def log_comando(comando: str, pessoa: str, key: dict):
    print("\n" + "=" * 60)
    print(f"👤 Pessoa : {pessoa}")
    print(f"💬 Comando : {comando}")
    print(f"🆔 ID : {key.get('id')}")
    print("=" * 60)


def converter_data(data_msg: str) -> datetime:
    try:
        return datetime.fromisoformat(data_msg.replace("Z", "+00:00"))
    except (AttributeError, ValueError, TypeError):
        return datetime.now()


# =====================================================
# WEBHOOK
# =====================================================
@app.route("/webhook", methods=["POST"])
def webhook():
    dados = request.json
    print("==========================================")
    print(dados)
    print("==========================================")
    print(dados["data"]["key"]["remoteJid"])
    print("==========================================")
    if not dados or dados.get("event") != "messages.upsert":
        return "OK"

    resultado = verificar_dados(dados)
    print(resultado)
    if resultado is None:
        return "OK"

    data = resultado["data"]
    key = resultado["key"]
    mensagem_raw = resultado["mensagem_raw"]
    pessoa = resultado["pessoa"]

    data_convertida = converter_data(dados.get("date_time", ""))
    print(data_convertida)

    data_convertida = converter_data(dados.get("date_time", ""))

    # Remove a informação de fuso horário
    agora = datetime.now()
    evento = data_convertida.replace(tzinfo=None)

    print("Agora     :", agora)
    print("Evento    :", evento)
    print("Diferença :", agora - evento)

    if agora - evento > timedelta(seconds=30):
        print(f"⏳ Mensagem antiga ignorada ({evento})")
        return "OK"
    log_comando(mensagem_raw, pessoa, key)

    mensagem = mensagem_raw.lower().strip()

    # ====================== COMANDOS ======================
    if mensagem in ("teste", "ping"):
        enviar_mensagem("✅ Sistema funcionando corretamente!", key["remoteJid"])

    elif mensagem in ("help", "ajuda"):
        texto =enviar_mensagem_help()
        enviar_mensagem(f"Digite *help <comando>* para mais detalhes.\n {texto} ", key["remoteJid"])
    
    elif mensagem.startswith("help") or mensagem.startswith("ajuda"):
        comando = mensagem.split()[1]
        enviar_mensagem(identificar_mensagem_help(comando),key["remoteJid"])
    
    elif mensagem.startswith("sobre"):
        enviar_mensagem(f"""*{NOME_BOT} v{VERSAO}*\n
Seu assistente inteligente para controle financeiro.\n
✅ Registro de entradas e gastos\n
✅ Controle de dívidas e parcelados\n
👨‍💻 Criado por: {CRIADOR}""", key["remoteJid"])

    elif mensagem.startswith("entrada"):
        #resposta = registrar_entrada(mensagem_raw, pessoa, data_convertida)
        enviar_mensagem(resposta, key["remoteJid"])

    elif mensagem.startswith("gasto"):
        #resposta = registrar_gasto(mensagem_raw, pessoa, data_convertida)
        enviar_mensagem(resposta, key["remoteJid"])

    else:
        enviar_mensagem("❓ Comando não reconhecido. Digite *help*", key["remoteJid"])

    return "OK"


# =====================================================
if __name__ == "__main__":
    WSGIRequestHandler.log_request = lambda *args, **kwargs: None
    logging.getLogger("werkzeug").setLevel(logging.ERROR)
    
    print("=" * 60)
    print(f"🤖 {NOME_BOT} v{VERSAO}")
    print(f"Host : {HOST}:{PORTA}")
    print("=" * 60)
    print("✅ Aguardando mensagens...\n")
    
    app.run(host=HOST, port=PORTA, debug=DEBUG, use_reloader=False)