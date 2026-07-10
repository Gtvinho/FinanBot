# database/db.py
import sqlite3
from pathlib import Path

DB_PATH = Path("financeiro2.db")

def get_connection():
    """Retorna uma conexão com o banco de dados."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Ativa Foreign Keys
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Inicializa o banco de dados (cria tabelas se não existirem)."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Aqui você pode colocar a criação das tabelas no futuro
    print("✅ Banco de dados conectado com sucesso.")
    conn.close()