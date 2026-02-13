from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models.cliente import Cliente, Base
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

class DatabaseManager:
    def __init__(self):
        host = os.getenv('DB_HOST')
        db = os.getenv('DB_NAME')
        user = os.getenv('DB_USER')
        password = quote_plus(os.getenv('DB_PASSWORD'))
        port = int(os.getenv('DB_PORT'))
        
        url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
        
        self.engine = create_engine(
            url,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            echo=True
        )
        
        # Cria as tabelas
        Base.metadata.create_all(self.engine)
        
        # Cria sessão
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def get_session(self):
        return self.session
    
    def close(self):
        self.session.close()