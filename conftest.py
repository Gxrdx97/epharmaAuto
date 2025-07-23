# conftest.py

import pytest
import tempfile
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

# 1. Registrando as opções de linha de comando para o Pytest
def pytest_addoption(parser):
    """Adiciona opções de linha de comando ao Pytest."""
    parser.addoption("--browser", action="store", default="chrome", help="Navegador para executar os testes (chrome ou firefox)")
    parser.addoption("--headless", action="store", default="No", help="Executar em modo headless (Yes/No)")

# 2. Refatorando a criação de options para suportar múltiplos navegadores
def get_browser_options(browser_name, headless):
    """Configura as options para o navegador selecionado."""
    browser_name = browser_name.lower()
    
    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        if headless.lower() == "yes":
            options.add_argument("--headless=new")
    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        if headless.lower() == "yes":
            options.add_argument("-headless")
    else:
        raise ValueError(f"Navegador '{browser_name}' não suportado.")

    # Opções gerais para melhorar a estabilidade
    options.add_argument("--incognito")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    # Isola o perfil do navegador para cada sessão de teste
    user_data_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    # Anexa o diretório para limpeza posterior
    options.user_data_dir = user_data_dir

    return options

# 3. Refatorando a criação do driver para ser uma fábrica
def get_driver(browser_name, options):
    """Cria a instância do WebDriver apropriado."""
    browser_name = browser_name.lower()
    
    if browser_name == "chrome":
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    elif browser_name == "firefox":
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
    else:
        # A verificação em get_browser_options já deve ter capturado isso
        raise ValueError(f"Navegador '{browser_name}' não suportado.")
        
    return driver

# 4. Fixture principal do navegador, agora mais limpa e flexível
@pytest.fixture(scope="function")
def browser(request):
    """Fixture principal que monta e desmonta o driver do Selenium."""
    # Pegando os valores da linha de comando
    browser_name = request.config.getoption("browser")
    headless = request.config.getoption("headless")
    
    # Montagem do ambiente
    options = get_browser_options(browser_name, headless)
    driver = get_driver(browser_name, options)
    
    driver.implicitly_wait(10)
    driver.maximize_window()

    try:
        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
    except TimeoutException:
        driver.quit() # Garante que o driver seja fechado em caso de falha
        pytest.fail("Erro crítico: A página não carregou no tempo esperado.", pytrace=False)

    # Disponibiliza o driver para os testes
    yield driver

    # Desmontagem e limpeza
    driver.quit()
    user_data_dir = getattr(options, "user_data_dir", None)
    if user_data_dir:
        shutil.rmtree(user_data_dir, ignore_errors=True)