from mensagens_automaticas.help_comandos_simples import *
def identificar_mensagem_help(comando): 
    match(comando): 
        case"entrada":
            return(enviar_mensagem_help_entrada())
        case"gasto":
            return(enviar_mensagem_help_gasto())
        case"divida":
            return(enviar_mensagem_help_divida())
        case"extrato":
            return(enviar_mensagem_help_extrato())
        case"parcelas":
            return(enviar_mensagem_help_parcelas())
        case _:
            return "Comando nao identificado"

