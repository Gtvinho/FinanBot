from flask import Flask, request
from datetime import datetime
import logging
import requests
from werkzeug.serving import WSGIRequestHandler

# ====================== IMPORTS DA NOVA ESTRUTURA ======================
# Database
from database.db import *
from database.clientes import *
from database.usuarios import *
from database.conversas import *
from database.movimentacoes import *
from database.parcelados import *
from database.dividas import *
from database.pagamentos import *

# Comandos
from comandos.registrar_entrada import registrar_entrada
from comandos.registrar_gasto import registrar_gasto
from comandos.registrar_vale import registrar_vale
from comandos.registrar_credito_parcelado import registrar_credito_parcelado
from comandos.registrar_divida import registrar_divida

# Consultas
from consultar_gastos.consultar_gastos import consultar_gastos
from consultar_gastos.consultar_parcelas import *  # se existir

# Funções Administrativas
from funcoes_administrativas.adm_find import encontrar_comando_administrativo
from funcoes_administrativas.delete import *

# Mensagens basicas do sistema
from mensagens_automaticas import gerenciador_mensagens
from mensagens_automaticas.help import *

#systema
from systema.verificacao import verificar_dados
# =====================================================
# INFORMAÇÕES DO SISTEMA
# =====================================================
NOME_BOT = "Financeiro Bot"
VERSAO = "1.2.0"
CRIADOR = "Gustavo Franzen Elicker"
ANO = "2026"

# =====================================================
# CONFIGURAÇÃO
# =====================================================
app = Flask(__name__)
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
    return f"🤖 *ROBO EM HOMOLOGACAO :*\n\n{texto}"


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
    print(f"🆔 ID : {key.get('id')}")
    print("=" * 60)


# =====================================================
# WEBHOOK
# =====================================================
@app.route("/webhook", methods=["POST"])
def webhook():
    dados = request.json
    
    # Validação inicial dos dados
    resultado = verificar_dados(dados)
    if resultado is None:
        return "OK"

    # Desempacotando dados validados
    data = resultado["data"]
    key = resultado["key"]
    mensagem = resultado["mensagem_raw"]
    pessoa = resultado["pessoa"]
    
    data_convertida = converter_data(dados.get("date_time", ""))
    
    log_comando(mensagem, pessoa, key)
    # ====================== COMANDOS ======================
    if mensagem in ("teste", "ping"):
        enviar_mensagem("✅ Sistema funcionando corretamente!")

    elif mensagem in ("help", "ajuda"):
        enviar_mensagem(enviar_mensagem_help())

    # Help específico
    elif mensagem.startswith(("help ", "ajuda ")):
        print("entrou no IF 1")
        comando = mensagem.split(maxsplit=1)[1]
        enviar_mensagem(gerenciador_mensagens.identificar_mensagem_help(comando))
        
    elif mensagem.startswith("sobre"):
        enviar_mensagem(f"""*{NOME_BOT} v{VERSAO}*\n
            Seu assistente inteligente para controle financeiro via Whatsapp.\n
            ✅ Registro de entradas e gastos\n
            ✅ Controle de créditos e dívidas\n
            ✅ Consultas e organização financeira\n
            ✅ Separação de gastos no cartão normal e vale alimentação\n
            ✅ Automação através do bot\n
            A versão 1.2 traz melhorias na organização dos registros...\n
            👨‍💻 Criado por: {CRIADOR}\n
            © {ANO} — Financeiro Bot""")

    elif mensagem.startswith("sudo"):
        if pessoa != "Gustavo F.":
            enviar_mensagem("sem permicao administrativa!")
        else:
            enviar_mensagem(encontrar_comando_administrativo(mensagem, pessoa))

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
    print(f"Host : {HOST}:{PORTA}")
    print("=" * 60)
    print("✅ Aguardando mensagens...\n")
    
    app.run(host=HOST, port=PORTA, debug=DEBUG, use_reloader=False)