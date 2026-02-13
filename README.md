# Gerenciamento de Clientes - Backend Python

Este projeto é um sistema de backend robusto desenvolvido em **Python** utilizando o framework **Flask**. Ele oferece uma API RESTful completa para o gerenciamento de clientes, integrando práticas modernas de desenvolvimento como DTOs, ORM e segurança de dados.

## 🚀 Funcionalidades

- **CRUD de Clientes**: Cadastro, listagem, busca por ID, atualização e exclusão.
- **Segurança**: Armazenamento de senhas criptografadas com `Bcrypt`.
- **Validação de Dados**: Verificação de CPF, unicidade de email e integridade de formulários.
- **Persistência**: Integração com banco de dados MySQL via SQLAlchemy.
- **Interface Web**: Frontend básico integrado para demonstração das funcionalidades.

## 📂 Estrutura do Projeto

```text
backend/
├── controllers/    # Lógica de negócio
├── database/       # Conexão e configuração do DB
├── dtos/           # Objetos de transferência de dados
├── models/         # Entidades do banco de dados
├── routers/        # Definição das rotas da API
├── static/         # Arquivos CSS e JS
├── templates/      # Interface HTML
├── app.py          # Arquivo principal
└── DOCUMENTACAO.md # Documentação técnica detalhada
```

## 🛠️ Pré-requisitos

- Python 3.11 ou superior
- MySQL Server
- Pip (Gerenciador de pacotes do Python)

## 🔧 Instalação e Configuração

1. **Clone o repositório ou extraia os arquivos:**
   ```bash
   cd projeto_backend_python/backend
   ```

2. **Crie um ambiente virtual (recomendado):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**
   Crie um arquivo `.env` na pasta `backend/` com as seguintes chaves:
   ```env
   DB_HOST=seu_host
   DB_NAME=seu_nome_banco
   DB_USER=seu_usuario
   DB_PASSWORD=sua_senha
   DB_PORT=3306
   ```

## 🏃 Execução

Para iniciar o servidor de desenvolvimento:

```bash
python app.py
```

O servidor estará disponível em `http://localhost:5000`.

## 📖 Documentação Adicional

Para detalhes técnicos sobre a arquitetura, endpoints da API e modelagem de dados, consulte o arquivo [DOCUMENTACAO.md](./backend/DOCUMENTACAO.md).

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.