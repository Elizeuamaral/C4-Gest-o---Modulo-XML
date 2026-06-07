from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Text
)

from sqlalchemy.orm import relationship

from database import Base


# =====================================================
# FORNECEDORES
# =====================================================

class Fornecedor(Base):
    __tablename__ = "fornecedores"

    id = Column(Integer, primary_key=True, index=True)

    cnpj = Column(String(18), unique=True, nullable=False)
    razao_social = Column(String(255), nullable=False)
    nome_fantasia = Column(String(255))

    endereco = Column(String(255))
    cidade = Column(String(100))
    estado = Column(String(2))

    telefone = Column(String(20))
    email = Column(String(150))

    criado_em = Column(DateTime, default=datetime.now)

    # Relacionamentos
    notas_fiscais = relationship(
        "NotaFiscal",
        back_populates="fornecedor",
        cascade="all, delete"
    )

    def __repr__(self):
        return f"<Fornecedor {self.razao_social}>"




# =====================================================
# NOTAS FISCAIS
# =====================================================

class NotaFiscal(Base):
    __tablename__ = "notas_fiscais"

    id = Column(Integer, primary_key=True, index=True)

    chave_acesso = Column(String(44), unique=True, nullable=False)

    numero_nota = Column(String(20))
    serie = Column(String(10))

    data_emissao = Column(DateTime)

    valor_total = Column(Float, default=0)

    cliente_nome = Column(String(255))

    cliente_documento = Column(String(20))

    data_importacao = Column(
        DateTime,
        default=datetime.utcnow
    )

    xml_path = Column(Text)

    fornecedor_id = Column(
        Integer,
        ForeignKey("fornecedores.id"),
        nullable=False
    )

    criado_em = Column(DateTime, default=datetime.utcnow)

    # Relacionamentos
    fornecedor = relationship(
        "Fornecedor",
        back_populates="notas_fiscais"
    )

    itens = relationship(
        "ItemNota",
        back_populates="nota_fiscal",
        cascade="all, delete-orphan"
    )

    logs = relationship(
        "LogImportacao",
        back_populates="nota_fiscal",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<NotaFiscal {self.numero_nota}>"




# =====================================================
# PRODUTOS
# =====================================================

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)

    codigo = Column(String(50), unique=True)
    descricao = Column(String(255), nullable=False)

    ncm = Column(String(20))
    cfop = Column(String(10))
    unidade = Column(String(10))

    criado_em = Column(DateTime, default=datetime.utcnow)

    # Relacionamentos
    itens = relationship(
        "ItemNota",
        back_populates="produto"
    )

    def __repr__(self):
        return f"<Produto {self.descricao}>"




# =====================================================
# ITENS DA NOTA
# =====================================================

class ItemNota(Base):
    __tablename__ = "itens_nota"

    id = Column(Integer, primary_key=True, index=True)

    nota_fiscal_id = Column(
        Integer,
        ForeignKey("notas_fiscais.id"),
        nullable=False
    )

    produto_id = Column(
        Integer,
        ForeignKey("produtos.id"),
        nullable=False
    )

    quantidade = Column(Float, nullable=False)
    valor_unitario = Column(Float, nullable=False)
    valor_total = Column(Float, nullable=False)

    criado_em = Column(DateTime, default=datetime.utcnow)

    # Relacionamentos
    nota_fiscal = relationship(
        "NotaFiscal",
        back_populates="itens"
    )

    produto = relationship(
        "Produto",
        back_populates="itens"
    )

    def __repr__(self):
        return f"<ItemNota Produto ID {self.produto_id}>"




# =====================================================
# LOGS DE IMPORTAÇÃO
# =====================================================

class LogImportacao(Base):
    __tablename__ = "logs_importacao"

    id = Column(Integer, primary_key=True, index=True)

    nota_fiscal_id = Column(
        Integer,
        ForeignKey("notas_fiscais.id")
    )

    status = Column(String(50))
    mensagem = Column(Text)

    criado_em = Column(DateTime, default=datetime.utcnow)

    # Relacionamentos
    nota_fiscal = relationship(
        "NotaFiscal",
        back_populates="logs"
    )

    def __repr__(self):
        return f"<LogImportacao {self.status}>"