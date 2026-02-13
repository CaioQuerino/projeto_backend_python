# dtos/cliente_dto.py
from datetime import datetime
from typing import Optional, Dict, Any

class RegistrarClienteDTO:
    """DTO para receber dados do formulário de cadastro"""
    
    def __init__(self, dados: Dict[str, Any]):
        self.email = dados.get('email', '').strip()
        self.nome = dados.get('name', '').strip()
        self.telefone = dados.get('number', '').strip()
        self.cpf = dados.get('cpf', '').strip()
        self.data_nascimento = dados.get('data', '')
        self.senha = dados.get('password', '')
        self.senha_c = dados.get('password_c', '')
    
    def validar_senhas(self) -> bool:
        """Valida se as senhas coincidem"""
        return self.senha == self.senha_c
    
    def validar_senha_tamanho(self, minimo: int = 6) -> bool:
        """Valida tamanho mínimo da senha"""
        return len(self.senha) >= minimo
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte DTO para dicionário (remove senha_c)"""
        return {
            'email': self.email,
            'nome': self.nome,
            'telefone': self.telefone,
            'cpf': self.cpf,
            'data_nascimento': self.data_nascimento,
            'senha': self.senha
        }
    
    def __repr__(self):
        return f"<RegistrarClienteDTO(email='{self.email}', nome='{self.nome}')>"


class ClienteResponseDTO:
    """DTO para enviar dados do cliente na resposta"""
    
    def __init__(self, cliente):
        self.id = cliente.id
        self.nome = cliente.nome
        self.email = cliente.email
        self.telefone = cliente.telefone
        self.cpf = cliente.cpf
        self.data_nascimento = cliente.data_nascimento
        self.data_cadastro = cliente.data_cadastro
        self.data_atualizacao = cliente.data_atualizacao
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário serializável"""
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'cpf': self.cpf,
            'data_nascimento': self.data_nascimento.strftime('%Y-%m-%d') if self.data_nascimento else None,
            'data_cadastro': self.data_cadastro.strftime('%Y-%m-%d %H:%M:%S') if self.data_cadastro else None,
            'data_atualizacao': self.data_atualizacao.strftime('%Y-%m-%d %H:%M:%S') if self.data_atualizacao else None
        }


class AtualizarClienteDTO:
    """DTO para atualização de cliente"""
    
    def __init__(self, dados: Dict[str, Any]):
        self.nome = dados.get('nome')
        self.email = dados.get('email')
        self.telefone = dados.get('telefone')
        self.data_nascimento = dados.get('data_nascimento')
    
    def to_dict(self) -> Dict[str, Any]:
        """Retorna apenas campos não nulos"""
        dados = {}
        if self.nome:
            dados['nome'] = self.nome
        if self.email:
            dados['email'] = self.email
        if self.telefone:
            dados['telefone'] = self.telefone
        if self.data_nascimento:
            dados['data_nascimento'] = self.data_nascimento
        return dados