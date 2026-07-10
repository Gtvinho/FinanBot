from database import get_connection

def deletar_entradas(descricao):
    print(descricao)
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM entradas WHERE descricao = ?",
        (descricao,)
    )

    conn.commit()

    return(f"{cursor.rowcount} registro(s) removido(s).")

    conn.close()