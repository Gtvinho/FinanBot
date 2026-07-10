# limpar_db.py
from database import get_connection

def limpar_banco():
    conn = get_connection()
    cursor = conn.cursor()
    
    print("🗑️ Limpando o banco de dados...")
    
    # Limpa os dados mas mantém a estrutura
    cursor.execute("DELETE FROM entradas;")
    cursor.execute("DELETE FROM gastos;")
    cursor.execute("DELETE FROM vales;")
    cursor.execute("DELETE FROM creditos_parcelados;")
    cursor.execute("DELETE FROM dividas;")
    
    conn.commit()
    conn.close()
    
    print("✅ Banco de dados limpo com sucesso!")

if __name__ == "__main__":
    confirmar = input("Tem certeza que deseja limpar TODOS os registros? (s/N): ")
    if confirmar.lower() == 's':
        limpar_banco()
    else:
        print("Operação cancelada.")