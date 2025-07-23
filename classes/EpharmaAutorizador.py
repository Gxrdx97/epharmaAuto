import os
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from classes.BrowserOptions import BrowserOptions

load_dotenv()


class EpharmaAutorizador(BrowserOptions):


    def __init__(self):
        """Inicializa as opções do EpharmaAutorizador."""
        super().__init__()
        self.url = os.getenv("URL_EPHARMA_AUTORIZADOR", "http://localhost:8000")
        self.login = os.environ.get("WEB_LOGIN", "default_login")
        self.password = os.environ.get("WEB_PASSWORD", "default_password")
        self.browser = self.browser()



    @staticmethod
    def get_url():
        """Retorna a URL do EpharmaAutorizador."""
        return EpharmaAutorizador.url

    @staticmethod
    def get_login():
        """Retorna o login do EpharmaAutorizador."""
        return EpharmaAutorizador.login

    @staticmethod
    def get_password():
        """Retorna a senha do EpharmaAutorizador."""
        return EpharmaAutorizador.password 
    



    @staticmethod
    def login(self):

        """Realiza o login no EpharmaAutorizador."""
        browser = self.browser
        browser.get(EpharmaAutorizador.get_url())
        
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#login"))
        ).send_keys(EpharmaAutorizador.get_login())

        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#senha"))
        ).send_keys(EpharmaAutorizador.get_password())
        
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-default.submit"))
        ).click()

        status_text = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modal.fade.ng-scope.ng-isolate-scope.show > div > div > div > div.row.top-buffer > p"))
        )

        if status_text:
            print(status_text.text)