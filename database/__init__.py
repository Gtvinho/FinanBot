# database/__init__.py

from .db import get_connection, init_db

# Importações específicas para evitar problemas
from .conversas import buscar_cliente_por_jid

# Importar o resto dos módulos
from .clientes import *
from .usuarios import *
from .movimentacoes import *
from .parcelados import *
from .dividas import *
from .licencas import *
from .pagamentos import *

__all__ = [
    'get_connection',
    'init_db',
    'buscar_cliente_por_jid',
]