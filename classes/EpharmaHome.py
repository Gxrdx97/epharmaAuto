import os
from EpharmaAutorizador import EpharmaAutorizador
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pydantic import BaseModel


class EpharmaHome(EpharmaAutorizador):
    def __init__(self):
        """Inicializa as opções da página inicial do Epharma."""
        super().__init__()
        self.url_home = os.getenv("URL_EPHARMA_HOME", "http://localhost:8000/home")
        


        
    def get_url(self):
        """Retorna a URL da página inicial do Epharma."""
        return EpharmaHome.url_home

    @staticmethod
    def navigate(self):
        browser = self.browser
        """Navega para a página inicial do Epharma."""
        browser.get(EpharmaHome.get_url())

    @staticmethod
    def nova_autorizacao(self):
        """Inicia uma nova autorização na página inicial."""
        browser = self.browser
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#side-bar > navi > a:nth-child(1)"))
        ).click()
        
        # Aqui você pode adicionar mais interações específicas para a nova autorização
        # Exemplo: preencher campos, clicar em botões, etc.    


    @staticmethod
    def consultar_autorizacao(self):
        """Consulta uma autorização existente na página inicial."""
        browser = self.browser
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#side-bar > navi > a:nth-child(5)"))
        ).click()
        
        # Aqui você pode adicionar mais interações específicas para a consulta de autorização
        # Exemplo: preencher campos de pesquisa, clicar em botões, etc.

    @staticmethod
    def cancelar_venda(self ):
        """Cancela uma venda na página inicial."""
        browser = self.browser
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#side-bar > navi > a:nth-child(9)"))
        ).click()
        
        # Aqui você pode adicionar mais interações específicas para o cancelamento de venda
        # Exemplo: preencher campos, clicar em botões, etc.    

    @staticmethod
    def transferir_imagens(self):
        """Transfere imagens na página inicial."""
        browser = self.browser
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#side-bar > navi > a:nth-child(13)"))
        ).click()
        
        # Aqui você pode adicionar mais interações específicas para a transferência de imagens
        # Exemplo: selecionar imagens, clicar em botões, etc.    


    @staticmethod
    def inserir_autorizacao(self, value):
        """Insere uma autorização na página inicial."""
        browser = self.browser
        dados_beneficiario = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='NumeroCartao']"))
        ).click()

        dados_beneficiario.send_keys(value)  

    @staticmethod
    def pesquisar_autorizacao(self):   
        browser = self.browser
        """Pesquisa uma autorização na página inicial."""
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-default"))
        ).click()


    @staticmethod
    def obter_status(self, text: str):

        """Obtém o status da autorização na página inicial."""
        browser = self.browser
        status_element = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".status-autorizacao"))
        )
        select = Select(status_element)
        select.select_by_visible_text(text)

    @staticmethod
    def selecionar_plano(self):
        """Seleciona o plano na página inicial."""
        browser = self.browser
        plano_element = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".cartao"))
        )
        plano_element.click()



    @staticmethod
    def insere_dados_autorizacao(self, dados: dict):
        """Insere os dados da autorização na página inicial."""
        browser = self.browser
        # Exemplo de como preencher campos com base no modelo de dados
        for field, value in dados.items():
            input_element = WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, field))
            )
            input_element.clear()
            input_element.send_keys(value)
        
        # Aqui você pode adicionar mais interações específicas para a inserção de dados
        # Exemplo: clicar em botões, selecionar opções, etc.        


        