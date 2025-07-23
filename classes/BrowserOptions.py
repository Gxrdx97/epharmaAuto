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




class BrowserOptions:

    """Classe para gerenciar as opções do navegador."""

    def __init__(self):
        """Inicializa as opções do navegador."""
        self.browser_name = "chrome"
        self.headless = "No"   


    def get_browser_options(self):
        """Configura as options para o navegador selecionado."""
        browser_name = self.browser_name.lower()
        headless = self.headless.lower()

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

    def get_driver(self, options):
        """Cria a instância do WebDriver apropriado."""
        browser_name = self.browser_name.lower()

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

    def browser(self):
      
        # Montagem do ambiente
        options = self.get_browser_options()
        driver = self.get_driver(options)

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
        return driver

       
    def close_browser(self, driver):
        """Fecha o navegador e limpa o diretório de dados do usuário."""
        driver.quit()
        if hasattr(driver, 'user_data_dir'):
            shutil.rmtree(driver.user_data_dir, ignore_errors=True)