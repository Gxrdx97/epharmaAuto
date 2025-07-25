from datetime import date
from typing import Optional
from pydantic import BaseModel
from classes.DatabaseManager import DatabaseManager
from sqlalchemy import text # Não se esqueça de importar!


class QueryExecutor:

    """Executa queries no banco de dados usando a sessão do DatabaseManager.
    Esta classe deve ser instanciada uma vez por aplicação.
    """

    def __init__(self):
        self.db = DatabaseManager()
        self.query =  """
            select v.valor ,vv.data_receita ,v.cliente, c.nome,c.cpf,c.observacoes,m.crm ,m.uf_conselho , epp.cod_prod, epp.prd_ean, Count(*) as quant ,cn.cod_barras_nfe  from e_pharma_cab epc 
            join vendas v on v.venda =epc.venda and v.empresa =epc.empresa
            join vendidos vv on vv.venda =v.venda and vv.empresa =v.empresa
            join e_pharma_prod epp  on epp.venda  =v.venda and epp.empresa =v.empresa
            join cab_nf cn on cn.venda = v.venda and cn.empresa =v.empresa 
            join clientes c on c.codigo =v.cliente
            join medico m on m.codigo =vv.nummedico
            where aut_venda=0 and cn.status_nfe =100  and epc.empresa =1
            group by v.valor,vv.data_receita,v.cliente, c.nome,c.cpf,c.observacoes,m.crm ,m.uf_conselho , epp.cod_prod, epp.prd_ean, cn.cod_barras_nfe

            """

    def execute_query(self, query: str = None):
        if not query:
            query = self.query
        if isinstance(query, str):
            query = text(query)        
        try:
            with self.db.get_session() as session:
                result = session.execute(query)
                return result.fetchall()
        except Exception as e:
            print(f"Erro ao executar a query: {e}")
            return None
        


    def query_rows(self, query: str = None):
        """Organiza a query para ser executada."""

        list_rows = []

        for row in self.execute_query(query= query):
           list_rows.append(row)

        return list_rows

    class ValoresAutorizacao(BaseModel): 
        """Modelo para os valores de autorização."""

        valor: float 
        data_receita: date
        cliente: float
        nome: str
        cpf: str
        observacoes: Optional[str] = None
        crm: float
        uf_conselho: str
        cod_prod: float
        prd_ean: float
        quant: int
        cod_barras_nfe: int     



    def set_valores_autorizacao(self, rows: list):
        """Processa todos os rows e retorna uma lista de ValoresAutorizacao."""

        autorizacoes = []
        for row in rows:
            autorizacao = self.ValoresAutorizacao(
                valor=row[0],
                data_receita=row[1],
                cliente=row[2],
                nome=row[3],
                cpf=row[4],
                observacoes=row[5],
                crm=row[6],
                uf_conselho=row[7],
                cod_prod=row[8],
                prd_ean=row[9],
                quant=row[10],
                cod_barras_nfe=row[11]
            )
            autorizacoes.append(autorizacao)
        return autorizacoes
        


    def return_functional_objects(self, query: str = None)-> list[ValoresAutorizacao]:
        """Retorna uma lista de objetos funcionais a partir dos rows."""
        
        rows = self.query_rows(query)
        return self.set_valores_autorizacao(rows)