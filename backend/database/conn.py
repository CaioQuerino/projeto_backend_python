import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.host = os.getenv('DB_HOST')
        self.db = os.getenv('DB_NAME')
        self.user = os.getenv('DB_USER')
        # Codifica a senha para URL
        self.password = quote_plus(os.getenv('DB_PASSWORD'))
        self.port = int(os.getenv('DB_PORT'))
        
        url = f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
        
        self.engine = create_engine(
            url,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            echo=False,
            # Adiciona connect_args para compatibilidade com MySQL 8
            connect_args={
                'charset': 'utf8mb4',
                'use_unicode': True,
                'ssl_disabled': True  # Desabilita SSL se não estiver usando
            }
        )
        self.connection = None
    
    def open_connection(self):
        try:
            self.connection = self.engine.connect()
            return self.connection
        except SQLAlchemyError as e:
            print(f"Erro ao conectar: {e}")
            raise
    
    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def test_connection(self):
        """Test if connection is working"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except SQLAlchemyError as e:
            print(f"Erro no teste de conexão: {e}")
            return False
    
    def __enter__(self):
        return self.open_connection()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

# Usage examples:
db = Database()

# Method 1: Traditional way
conn = db.open_connection()
if conn:
    print("Conectado com sucesso!")
    db.close_connection()

# Method 2: Test connection
if db.test_connection():
    print("Conexão OK!")
else:
    print("Falha na conexão!")