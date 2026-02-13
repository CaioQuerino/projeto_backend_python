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
    
    def atualizar_cliente(self, id, dados):
        """
        Atualiza dados de um cliente existente
        Args:
            id: ID do cliente
            dados: dict com campos a serem atualizados (nome, email, telefone, data_nascimento)
        """
        try:
            cliente = self.session.query(Cliente).filter_by(id=id).first()
            
            if not cliente:
                return {'success': False, 'message': 'Cliente não encontrado!'}
            
            if 'nome' in dados and dados['nome']:
                cliente.nome = dados['nome']
            
            if 'email' in dados and dados['email'] and dados['email'] != cliente.email:
                # Verifica se email já existe em outro cliente
                email_existente = self.session.query(Cliente).filter(
                    Cliente.email == dados['email'],
                    Cliente.id != id
                ).first()
                
                if email_existente:
                    return {'success': False, 'message': 'Email já cadastrado para outro cliente!'}
                
                cliente.email = dados['email']
            
            if 'telefone' in dados and dados['telefone']:
                cliente.telefone = Cliente.formatar_telefone(dados['telefone'])
            
            if 'data_nascimento' in dados and dados['data_nascimento']:
                cliente.data_nascimento = datetime.strptime(
                    dados['data_nascimento'], '%Y-%m-%d'
                ).date()
            
            if 'senha' in dados and dados['senha']:
                senha_hash = bcrypt.hashpw(
                    dados['senha'].encode('utf-8'),
                    bcrypt.gensalt()
                )
                cliente.senha_hash = senha_hash.decode('utf-8')
            
            cliente.data_atualizacao = datetime.now()
            
            self.session.commit()
            
            response_dto = ClienteResponseDTO(cliente)
            
            return {
                'success': True,
                'message': 'Cliente atualizado com sucesso!',
                'cliente': response_dto.to_dict()
            }
            
        except Exception as e:
            self.session.rollback()
            return {'success': False, 'message': f'Erro ao atualizar: {str(e)}'}
    
    def deletar_cliente(self, id):
        """
        Deleta um cliente do banco de dados
        Args:
            id: ID do cliente a ser deletado
        """
        try:
            cliente = self.session.query(Cliente).filter_by(id=id).first()
            
            if not cliente:
                return {'success': False, 'message': 'Cliente não encontrado!'}
            
            self.session.delete(cliente)
            self.session.commit()
            
            return {
                'success': True,
                'message': f'Cliente {cliente.nome} deletado com sucesso!'
            }
            
        except Exception as e:
            self.session.rollback()
            return {'success': False, 'message': f'Erro ao deletar: {str(e)}'}
    
    
    def contar_clientes(self):
        """Retorna o número total de clientes cadastrados"""
        try:
            total = self.session.query(Cliente).count()
            return {'success': True, 'total': total}
        except Exception as e:
            return {'success': False, 'message': f'Erro ao contar clientes: {str(e)}'}
    
    def buscar_por_nome(self, nome):
        """Busca clientes por nome (busca parcial)"""
        try:
            clientes = self.session.query(Cliente).filter(
                Cliente.nome.ilike(f'%{nome}%')
            ).all()
            
            return {
                'success': True,
                'clientes': [ClienteResponseDTO(cliente).to_dict() for cliente in clientes]
            }
        except Exception as e:
            return {'success': False, 'message': f'Erro ao buscar por nome: {str(e)}'}
    
    def buscar_por_periodo(self, data_inicio, data_fim):
        """Busca clientes cadastrados em um período"""
        try:
            clientes = self.session.query(Cliente).filter(
                Cliente.data_cadastro.between(data_inicio, data_fim)
            ).all()
            
            return {
                'success': True,
                'clientes': [ClienteResponseDTO(cliente).to_dict() for cliente in clientes]
            }
        except Exception as e:
            return {'success': False, 'message': f'Erro ao buscar por período: {str(e)}'}
    
    def __del__(self):
        """Fecha a sessão ao destruir o objeto"""
        if hasattr(self, 'db'):
            self.db.close()