
from classes.QueryExecutor import QueryExecutor



query_executor = QueryExecutor()

def test_get_query():
    """Retorna a query para o banco de dados."""


    query = """
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
    print(query_executor.return_functional_objects(query))
