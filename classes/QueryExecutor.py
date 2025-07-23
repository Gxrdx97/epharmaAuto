from classes.DatabaseManager import DatabaseManager
from sqlalchemy import text # Não se esqueça de importar!




class QueryExecutor:
    def __init__(self, db_connection: DatabaseManager):
        self.db = db_connection

        



    def execute_query(self, query: str):
        
        try:
            if isinstance(query, str):
                query = text(query)
            with self.db.get_session() as session:
                result = session.execute(query)
                return result.fetchall()
        except Exception as e:
            print(f"Erro ao executar a query: {e}")
            return None
        


