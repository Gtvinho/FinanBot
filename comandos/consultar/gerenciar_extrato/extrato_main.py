def consultar_extrato():
    mensagem = "mensagem"
    if a == mensagem.startswith("extrato"):
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