import os
from desktop_automation.epharma_init import initialize_epharma
from dotenv import load_dotenv

load_dotenv()

LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")

def test_login_epharma_plug_in():
    """Testa o login no Epharma Autorizador."""

    app = initialize_epharma()
    if not app:
        raise RuntimeError("Não foi possível iniciar a aplicação e-Pharma.")

    # 1. Crie a especificação para a janela principal
    main_window = app.window(title_re=".*e-Pharma.*") # Usar um regex no título é mais robusto

    # 2. Espere a janela estar pronta e traga-a para o foco
    main_window.wait('ready', timeout=20)
    main_window.set_focus()

    # # 3. Encontre o campo de usuário e interaja com ele
    # # Note como construímos o caminho completo antes da ação .click_input()
    user_field = main_window.child_window(auto_id="txtCNPJ", control_type="Edit")
    user_field.wait('visible', timeout=10) # Boa prática: espere o campo ser visível
    user_field.click_input()
    user_field.set_text("")  # Limpa o campo antes de digitar
    # Digite o usuário, com espaços se necessário
    user_field.set_text(LOGIN)

    # 4. Faça o mesmo para o campo de senha
    password_field = main_window.child_window(auto_id="txtNLicenca", control_type="Edit")
    password_field.wait('visible', timeout=10)
    password_field.click_input()
    password_field.set_text("")  # Limpa o campo antes de digitar
    password_field.set_text(PASSWORD)

    # 5. Clique no botão de login
    login_button = main_window.child_window(auto_id="btnAuthVerify", control_type="Button")
    login_button.wait('ready', timeout=10)
    login_button.click()

    status = main_window.child_window(auto_id="lblAuthStatus", control_type="Text").wait('visible', timeout=10)

    text_status = status.window_text()
    print(f"Status do login: {text_status}")
    
