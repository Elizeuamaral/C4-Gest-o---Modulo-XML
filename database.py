from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

import sys
from pathlib import Path

# =========================
# Caminho do banco SQLite
# =========================

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).resolve().parent

DB_DIR = BASE_DIR / "database"

DB_DIR.mkdir(exist_ok=True)

db_file = DB_DIR / "financeiro.db"

print("=" * 50)
print("BASE_DIR =", BASE_DIR)
print("DB_DIR =", DB_DIR)
print("DATABASE =", db_file)
print("=" * 50)

DATABASE_URL = f"sqlite:///{db_file}"

# =========================
# Engine
# =========================

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

# =========================
# Sessão
# =========================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True
)

# =========================
# Base ORM
# =========================

Base = declarative_base()


# =========================
# Inicialização do banco
# =========================

def init_db():
    from models import (
        Fornecedor,
        NotaFiscal,
        Produto,
        ItemNota,
        LogImportacao
    )

    Base.metadata.create_all(bind=engine)