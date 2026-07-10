from database import get_connection

def limpar_banco():
    conn = get_connection()
    cursor = conn.cursor()
    
    print("⚠️  ATENÇÃO: Isso vai apagar TODOS os dados!")
    if input("Digite 'SIM' para confirmar: ").upper() != "SIM":
        print("Cancelado.")
        return
    
    cursor.execute("DELETE FROM gastos")
    cursor.execute("DELETE FROM entradas")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('gastos', 'entradas')")
    
    conn.commit()
    conn.close()
    print("✅ Banco limpo com sucesso!")

if __name__ == "__main__":
    limpar_banco()