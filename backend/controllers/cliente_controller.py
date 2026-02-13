# controllers/cliente_controller.py
from models.cliente import Cliente
from database.models import DatabaseManager
from dtos.cliente_dto import ClienteResponseDTO
from datetime import datetime
import bcrypt

class ClienteController:
    def __init__(self):
        self.db = DatabaseManager()
        self.session = self.db.get_session()
    
    def cadastrar_cliente(self, dados):
        """
        Cadastra um novo cliente
        dados: dict com email, nome, telefone, cpf, data_nascimento, senha
        """
        try:
            # Validações
            if not Cliente.validar_cpf(dados['cpf']):
                return {'success': False, 'message': 'CPF inválido!'}
            
            # Verifica se email já existe
            if self.session.query(Cliente).filter_by(email=dados['email']).first():
                return {'success': False, 'message': 'Email já cadastrado!'}
            
            # Verifica se CPF já existe
            if self.session.query(Cliente).filter_by(cpf=dados['cpf']).first():
                return {'success': False, 'message': 'CPF já cadastrado!'}
            
            # Criptografa senha
            senha_hash = bcrypt.hashpw(
                dados['senha'].encode('utf-8'), 
                bcrypt.gensalt()
            )
            
            # Formata dados
            telefone_formatado = Cliente.formatar_telefone(dados['telefone'])
            cpf_formatado = Cliente.formatar_cpf(dados['cpf'])
            
            # Cria novo cliente
            novo_cliente = Cliente(
                nome=dados['nome'],
                email=dados['email'],
                telefone=telefone_formatado,
                cpf=cpf_formatado,
                data_nascimento=datetime.strptime(dados['data_nascimento'], '%Y-%m-%d').date(),
                senha_hash=senha_hash.decode('utf-8')
            )
            
            self.session.add(novo_cliente)
            self.session.commit()
            
            # Usa DTO de resposta
            response_dto = ClienteResponseDTO(novo_cliente)
            
            return {
                'success': True, 
                'message': 'Cliente cadastrado com sucesso!', 
                'cliente': response_dto.to_dict()
            }
            
        except Exception as e:
            self.session.rollback()
            return {'success': False, 'message': f'Erro ao cadastrar: {str(e)}'}
    
    def listar_clientes(self):
        """Lista todos os clientes"""
        try:
            clientes = self.session.query(Cliente).all()
            # Usa DTO de resposta para cada cliente
            return {
                'success': True, 
                'clientes': [ClienteResponseDTO(cliente).to_dict() for cliente in clientes]
            }
        except Exception as e:
            return {'success': False, 'message': f'Erro ao listar: {str(e)}'}
    
    def buscar_cliente(self, id=None, email=None, cpf=None):
        """Busca cliente por ID, email ou CPF"""
        try:
            cliente = None
            if id:
                cliente = self.session.query(Cliente).filter_by(id=id).first()
            elif email:
                cliente = self.session.query(Cliente).filter_by(email=email).first()
            elif cpf:
                cliente = self.session.query(Cliente).filter_by(cpf=cpf).first()
            
            if cliente:
                response_dto = ClienteResponseDTO(cliente)
                return {'success': True, 'cliente': response_dto.to_dict()}
            return {'success': True, 'cliente': None}
            
        except Exception as e:
            return {'success': False, 'message': f'Erro ao buscar: {str(e)}'}
    
    # ... resto do código (atualizar, deletar) permanece igual, usando ClienteResponseDTO