# systema/verificacao.py
from database.users_server_banco.usuarios import buscar_cliente_por_jid


def verificar_dados(dados: dict):
    """
    Valida os dados do webhook e retorna as informações principais.
    Retorna None se não for uma mensagem válida.
    """
    if not dados or dados.get("event") != "messages.upsert":
        return None

    data = dados.get("data", {})
    key = data.get("key", {})
    message = data.get("message", {})

    if "senderKeyDistributionMessage" in message:
        return None

    usuario = buscar_cliente_por_jid(key.get("remoteJid"))
    if usuario is None:
        return None
    else: 
        print("usuario aqui: ",usuario)
    mensagem_raw = message.get("conversation")
    if not mensagem_raw:
        return None

    mensagem_raw = mensagem_raw.strip()

    return {
        "data": data,
        "key": key,
        "message": message,
        "mensagem_raw": mensagem_raw,
        "cliente": usuario,
        "pessoa": data.get("pushName", "Desconhecido")
    }