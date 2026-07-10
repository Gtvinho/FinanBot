import sqlite3

DB = "financeiro2.db"

conn = sqlite3.connect(DB)
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

# =====================================================
# CLIENTES
# =====================================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nome TEXT NOT NULL,

    plano TEXT NOT NULL DEFAULT 'Individual',

    status TEXT NOT NULL DEFAULT 'Ativo',

    validade DATE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# =====================================================
# USUÁRIOS
# =====================================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    cliente_id INTEGER NOT NULL,

    nome TEXT NOT NULL,

    telefone TEXT,

    administrador INTEGER DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(cliente_id)
        REFERENCES clientes(id)
        ON DELETE CASCADE
)
""")

# =====================================================
# CONVERSAS
# =====================================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS conversas (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    cliente_id INTEGER NOT NULL,

    jid TEXT NOT NULL UNIQUE,

    tipo TEXT NOT NULL CHECK(tipo IN ('grupo','individual')),

    ativo INTEGER DEFAULT 1,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(cliente_id)
        REFERENCES clientes(id)
        ON DELETE CASCADE
)
""")

# =====================================================
# MOVIMENTAÇÕES
# =====================================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS movimentacoes (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    cliente_id INTEGER NOT NULL,

    usuario_id INTEGER NOT NULL,

    data TIMESTAMP NOT NULL,

    tipo TEXT NOT NULL CHECK(tipo IN ('entrada','gasto','vale')),

    forma_pagamento TEXT NOT NULL,

    descricao TEXT NOT NULL,

    valor REAL NOT NULL CHECK(valor >= 0),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(cliente_id)
        REFERENCES clientes(id)
        ON DELETE CASCADE,

    FOREIGN KEY(usuario_id)
        REFERENCES usuarios(id)
)
""")

# =====================================================
# PARCELADOS
# =====================================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS parcelados (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    cliente_id INTEGER NOT NULL,

    usuario_id INTEGER NOT NULL,

    data_compra TIMESTAMP NOT NULL,

    descricao TEXT NOT NULL,

    valor_total REAL NOT NULL CHECK(valor_total > 0),

    num_parcelas INTEGER NOT NULL CHECK(num_parcelas > 0),

    valor_parcela REAL NOT NULL,

    parcela_atual INTEGER DEFAULT 1,

    parcelas_pagas INTEGER DEFAULT 0,

    mes_inicio INTEGER NOT NULL,

    ano_inicio INTEGER NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(cliente_id)
        REFERENCES clientes(id)
        ON DELETE CASCADE,

    FOREIGN KEY(usuario_id)
        REFERENCES usuarios(id)
)
""")

# =====================================================
# DÍVIDAS
# =====================================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS dividas (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    cliente_id INTEGER NOT NULL,

    usuario_id INTEGER NOT NULL,

    descricao TEXT NOT NULL,

    valor REAL NOT NULL CHECK(valor > 0),

    status TEXT DEFAULT 'aberta'
        CHECK(status IN ('aberta','quitada')),

    data TIMESTAMP NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(cliente_id)
        REFERENCES clientes(id)
        ON DELETE CASCADE,

    FOREIGN KEY(usuario_id)
        REFERENCES usuarios(id)
)
""")

# =====================================================
# PLANOS
# =====================================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS planos (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nome TEXT NOT NULL,

    valor REAL NOT NULL,

    dias_tolerancia INTEGER DEFAULT 30
)
""")

# =====================================================
# LICENÇAS
# =====================================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS licencas (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    cliente_id INTEGER NOT NULL,

    plano_id INTEGER NOT NULL,

    inicio DATE NOT NULL,

    vencimento DATE NOT NULL,

    status TEXT DEFAULT 'ativa'
        CHECK(status IN ('ativa','bloqueada','cancelada')),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(cliente_id)
        REFERENCES clientes(id)
        ON DELETE CASCADE,

    FOREIGN KEY(plano_id)
        REFERENCES planos(id)
)
""")

# =====================================================
# PAGAMENTOS
# =====================================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS pagamentos (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    cliente_id INTEGER NOT NULL,

    valor REAL NOT NULL,

    data_pagamento DATE,

    forma TEXT,

    observacao TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(cliente_id)
        REFERENCES clientes(id)
        ON DELETE CASCADE
)
""")

# =====================================================
# CONFIGURAÇÕES
# =====================================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS configuracoes (

    cliente_id INTEGER PRIMARY KEY,

    nome_bot TEXT DEFAULT 'Financeiro Bot',

    moeda TEXT DEFAULT 'BRL',

    mostrar_vale INTEGER DEFAULT 1,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(cliente_id)
        REFERENCES clientes(id)
        ON DELETE CASCADE
)
""")

conn.commit()
conn.close()

print("✅ Banco criado com sucesso!")