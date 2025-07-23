from typing import Generator
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager

class DatabaseManager:
    """
    Gerencia a configuração do banco de dados e a criação de sessões.
    Esta classe deve ser instanciada uma vez por aplicação.
    """
    def __init__(self):
        # 1. A configuração acontece uma única vez, na inicialização.
        credentials = self._get_credentials()
        
        # A engine é o coração da conexão, é criada apenas uma vez.
        self.engine = create_engine(
            f"mysql+pymysql://{credentials['user']}:{credentials['password']}"
            f"@{credentials['host']}:{credentials['port']}/{credentials['database']}"
        )
        
        # 2. A sessionmaker é a nossa "fábrica" de sessões, configurada uma vez.
        self._session_factory = sessionmaker(bind=self.engine)

    def _get_credentials(self) -> dict:
        """Obtém as credenciais do banco de dados a partir de variáveis de ambiente."""
        return {
            "user": os.getenv("DB_USER", "default_user"),
            "password": os.getenv("DB_PASSWORD", "default_password"),
            "host": os.getenv("DB_HOST", "localhost"),
            "port": os.getenv("DB_PORT", "3306"), # Porta padrão do MySQL
            "database": os.getenv("DB_NAME", "mydatabase")
        }


    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """
        Fornece uma nova sessão do banco de dados de forma segura.
        Isso implementa o padrão "Unit of Work".
        """
        session = self._session_factory() # Cria um novo "balcão de atendimento"
        try:
            yield session
            session.commit() # Confirma a transação se tudo deu certo
        except Exception:
            session.rollback() # Desfaz em caso de erro
            raise
        finally:
            session.close() # Sempre fecha a sessão para liberar recursos