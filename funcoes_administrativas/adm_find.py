from funcoes_administrativas.delete import * 
from funcoes_administrativas.delete import * 

def filtrar_funcao(mensagem):
    partes = mensagem.split()
    if len(partes) < 4:
        return "Erro: formato inválido."
    if partes[0] != "sudo" or partes[1] != "--delete":
        return "Erro: formato inválido."
    return " ".join(partes[3:])

def encontrar_comando_administrativo(mensagem, pessoa): 
    #define qual funcao de banco usar
    if "--delete" in mensagem: 

        #filtra parametro de descricao
        descricao = filtrar_funcao(mensagem)
        if descricao ==  "Erro: formato inválido.":
                return descricao
        #define tipo de tabela que vai ser usada
        if "-entrada" in mensagem:
            return deletar_entradas(descricao)
        elif "-gasto" in mensagem: 
            pass
        elif "-parcelas" in mensagem:
            pass
        else: 
            return "Erro: formato inválido."




    else: 
        mesnsagem_retorno = "especifique o comando"
    return mesnsagem_retorno        