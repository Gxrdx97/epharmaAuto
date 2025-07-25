from classes.EpharmaHome import EpharmaHome
from classes.QueryExecutor import QueryExecutor
epharma_home = EpharmaHome()
query_executor = QueryExecutor()

list_autorizacoes = query_executor.return_functional_objects()





def test_insere_autorizacao_epharma_web():

    
    try:
        epharma_home.inserir_autorizacao(value="034.448.389-48")

        epharma_home.pesquisar_autorizacao()

    except Exception as e:
        print(f"Erro ao realizar nova autorização: {e}")