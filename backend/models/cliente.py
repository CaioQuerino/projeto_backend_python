from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'clientes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    telefone = Column(String(20), nullable=False)
    cpf = Column(String(14), nullable=False, unique=True)
    data_nascimento = Column(Date, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    data_cadastro = Column(DateTime, default=datetime.now)
    data_atualizacao = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f"<Cliente(nome='{self.nome}', email='{self.email}')>"
    
    @staticmethod
    def validar_cpf(cpf):
        """Validação básica de CPF"""
        cpf = ''.join(filter(str.isdigit, cpf))
        if len(cpf) != 11:
            return False
        return True
    
    @staticmethod
    def formatar_telefone(telefone):
        """Formata telefone para padrão (XX) XXXXX-XXXX"""
        telefone = ''.join(filter(str.isdigit, telefone))
        if len(telefone) == 11:
            return f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"
        elif len(telefone) == 10:
            return f"({telefone[:2]}) {telefone[2:6]}-{telefone[6:]}"
        return telefone
    
    @staticmethod
    def formatar_cpf(cpf):
        """Formata CPF para padrão XXX.XXX.XXX-XX"""
        cpf = ''.join(filter(str.isdigit, cpf))
        if len(cpf) == 11:
            return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        return cpf