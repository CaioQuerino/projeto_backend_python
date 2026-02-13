# routers/cliente_router.py
from flask import Blueprint, request, jsonify
from controllers.cliente_controller import ClienteController
from dtos.cliente_dto import RegistrarClienteDTO, AtualizarClienteDTO

cliente_bp = Blueprint('clientes', __name__, url_prefix='/api/clientes')
cliente_controller = ClienteController()

@cliente_bp.route('', methods=['POST'])
def cadastrar_cliente():
    try:
        # Valida campos obrigatórios
        campos_obrigatorios = ['email', 'name', 'number', 'cpf', 'data', 'password', 'password_c']
        for campo in campos_obrigatorios:
            if not request.form.get(campo):
                return jsonify({
                    'success': False,
                    'message': f'Campo {campo} é obrigatório!'
                }), 400
        
        # Cria DTO com os dados do formulário
        cliente_dto = RegistrarClienteDTO(request.form)
        
        # Validações
        if not cliente_dto.validar_senha_tamanho():
            return jsonify({
                'success': False,
                'message': 'Senha deve ter no mínimo 6 caracteres!'
            }), 400
        
        if not cliente_dto.validar_senhas():
            return jsonify({
                'success': False,
                'message': 'As senhas não coincidem!'
            }), 400
        
        # Chama o controller com os dados do DTO
        resultado = cliente_controller.cadastrar_cliente(cliente_dto.to_dict())
        
        status_code = 201 if resultado['success'] else 400
        return jsonify(resultado), status_code
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro no servidor: {str(e)}'
        }), 500

@cliente_bp.route('', methods=['GET'])
def listar_clientes():
    resultado = cliente_controller.listar_clientes()
    return jsonify(resultado), 200 if resultado['success'] else 400

@cliente_bp.route('/<int:id>', methods=['GET'])
def buscar_cliente(id):
    resultado = cliente_controller.buscar_cliente(id=id)
    if resultado['success'] and resultado['cliente']:
        return jsonify(resultado), 200
    return jsonify({'success': False, 'message': 'Cliente não encontrado!'}), 404

@cliente_bp.route('/<int:id>', methods=['PUT'])
def atualizar_cliente(id):
    try:
        # Cria DTO de atualização
        dados = request.json if request.is_json else request.form.to_dict()
        atualizar_dto = AtualizarClienteDTO(dados)
        
        resultado = cliente_controller.atualizar_cliente(id, atualizar_dto.to_dict())
        return jsonify(resultado), 200 if resultado['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@cliente_bp.route('/<int:id>', methods=['DELETE'])
def deletar_cliente(id):
    resultado = cliente_controller.deletar_cliente(id)
    return jsonify(resultado), 200 if resultado['success'] else 404