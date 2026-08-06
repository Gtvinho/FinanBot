-- =============================================
-- SCHEMA FINAL - Financeiro Bot
-- Gerado em: Julho/2026
-- =============================================

PRAGMA foreign_keys = ON;

-- =============================================
-- TABELA CLIENTES
-- =============================================
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    plano TEXT NOT NULL DEFAULT 'Individual',
    status TEXT NOT NULL DEFAULT 'Ativo',
    validade DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- TABELA USUARIOS
-- =============================================
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    nome TEXT NOT NULL,
    telefone TEXT,
    jid TEXT UNIQUE,
    administrador INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
);

-- =============================================
-- TABELA CONVERSAS
-- =============================================
CREATE TABLE conversas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    jid TEXT NOT NULL UNIQUE,
    nome TEXT,
    tipo TEXT NOT NULL CHECK(tipo IN ('grupo','individual')),
    ativo INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
);

-- =============================================
-- TABELA CONTAS
-- =============================================
CREATE TABLE contas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    nome TEXT NOT NULL,
    tipo TEXT NOT NULL,
    banco TEXT,
    saldo_inicial REAL DEFAULT 0.0,
    limite REAL DEFAULT 0.0,
    dia_fechamento INTEGER CHECK(dia_fechamento BETWEEN 1 AND 31),
    dia_vencimento INTEGER CHECK(dia_vencimento BETWEEN 1 AND 31),
    ativo INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
);

-- =============================================
-- TABELA CATEGORIAS
-- =============================================
CREATE TABLE categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    ativo INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- TABELA FORMAS_PAGAMENTO
-- =============================================
CREATE TABLE formas_pagamento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    ativo INTEGER DEFAULT 1
);

-- =============================================
-- TABELA MOVIMENTACOES
-- =============================================
CREATE TABLE movimentacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL,
    conta_id INTEGER,
    categoria_id INTEGER,
    forma_pagto_id INTEGER,
    data TIMESTAMP NOT NULL,
    tipo TEXT NOT NULL CHECK(tipo IN ('entrada','gasto','vale')),
    forma_pagamento TEXT NOT NULL,
    descricao TEXT NOT NULL,
    valor REAL NOT NULL CHECK(valor >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (conta_id) REFERENCES contas(id) ON DELETE SET NULL,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE SET NULL,
    FOREIGN KEY (forma_pagto_id) REFERENCES formas_pagamento(id) ON DELETE SET NULL
);

-- =============================================
-- TABELA PARCELADOS
-- =============================================
CREATE TABLE parcelados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL,
    conta_id INTEGER,
    categoria_id INTEGER,
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
    
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (conta_id) REFERENCES contas(id) ON DELETE SET NULL,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE SET NULL
);

-- =============================================
-- TABELA DIVIDAS
-- =============================================
CREATE TABLE dividas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL,
    categoria_id INTEGER,
    descricao TEXT NOT NULL,
    valor REAL NOT NULL CHECK(valor > 0),
    status TEXT DEFAULT 'aberta' CHECK(status IN ('aberta','quitada')),
    data TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE SET NULL
);

-- =============================================
-- TABELAS DE PLANOS E LICENÇAS
-- =============================================
CREATE TABLE planos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    valor REAL NOT NULL,
    dias_tolerancia INTEGER DEFAULT 30
);

CREATE TABLE licencas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    plano_id INTEGER NOT NULL,
    inicio DATE NOT NULL,
    vencimento DATE NOT NULL,
    status TEXT DEFAULT 'ativa' CHECK(status IN ('ativa','bloqueada','cancelada')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE,
    FOREIGN KEY (plano_id) REFERENCES planos(id)
);

CREATE TABLE pagamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    valor REAL NOT NULL,
    data_pagamento DATE,
    forma TEXT,
    observacao TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
);

-- =============================================
-- TABELA CONFIGURACOES
-- =============================================
CREATE TABLE configuracoes (
    cliente_id INTEGER PRIMARY KEY,
    nome_bot TEXT DEFAULT 'Financeiro Bot',
    moeda TEXT DEFAULT 'BRL',
    mostrar_vale INTEGER DEFAULT 1,
    timezone TEXT DEFAULT 'America/Sao_Paulo',
    idioma TEXT DEFAULT 'pt-BR',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
);

-- =============================================
-- ÍNDICES PARA PERFORMANCE
-- =============================================
CREATE INDEX IF NOT EXISTS idx_movimentacoes_data ON movimentacoes(data);
CREATE INDEX IF NOT EXISTS idx_movimentacoes_cliente ON movimentacoes(cliente_id);
CREATE INDEX IF NOT EXISTS idx_parcelados_cliente ON parcelados(cliente_id);
CREATE INDEX IF NOT EXISTS idx_contas_cliente ON contas(cliente_id);
CREATE INDEX IF NOT EXISTS idx_dividas_cliente ON dividas(cliente_id);