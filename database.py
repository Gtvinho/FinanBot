# database.py
import sqlite3
from pathlib import Path

DB_PATH = Path("financeiro.db")

def get_connection():
    """Retorna uma conexão com o banco de dados"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome (dict-like)
    return conn


def init_database():
    """Cria as tabelas caso não existam"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tabela Entradas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entradas (
        id INTEGER PRIMARY KEY,
        data TEXT,
        pessoa TEXT,
        origem TEXT,
        categoria TEXT DEFAULT 'salario',
        descricao TEXT,
        valor REAL
    )
    """)

    # Tabela Gastos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gastos (
        id INTEGER PRIMARY KEY,
        data TEXT,
        pessoa TEXT,
        descricao TEXT,
        categoria TEXT,
        forma_pagamento TEXT,
        valor REAL
    )
    """)

    # Tabela Dívidas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dividas (
        id INTEGER PRIMARY KEY,
        data TEXT,
        descricao TEXT,
        valor REAL,
        status TEXT DEFAULT 'aberta'
    )
    """)

    # Tabela Crédito Parcelado
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS creditos_parcelados (
        id INTEGER PRIMARY KEY,
        data_compra TEXT,
        descricao TEXT,
        valor_total REAL,
        num_parcelas INTEGER,
        valor_parcela REAL,
        parcela_atual INTEGER DEFAULT 1,
        registrado_por TEXT
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Banco de dados inicializado com sucesso!")