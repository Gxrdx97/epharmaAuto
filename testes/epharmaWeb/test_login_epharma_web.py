from classes.EpharmaHome import EpharmaHome




epharma_home = EpharmaHome()

def test_login_epharma_web():

    try:
        epharma_home.login()

    except Exception as e:
        print(f"Erro ao realizar login: {e}")


def test_nova_autorizacao_epharma_web():
    try:
        epharma_home.inserir_autorizacao(value="034.448.389-48")

        epharma_home.pesquisar_autorizacao()

    except Exception as e:
        print(f"Erro ao realizar nova autorização: {e}")