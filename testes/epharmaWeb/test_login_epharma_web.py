from classes.EpharmaHome import EpharmaHome


epharma_home = EpharmaHome()

def test_login_epharma_web():   
    try:
        epharma_home.login()

    except Exception as e:
        print(f"Erro ao realizar login: {e}")


