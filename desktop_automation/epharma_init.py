import os
import time
from dotenv import load_dotenv
from pywinauto.application import Application,ProcessNotFoundError
from pywinauto import Desktop



load_dotenv()

REAL_EXE_PATH = os.getenv("REAL_EXE_PATH", r"C:\Users\gabri\AppData\Local\Apps\2.0\RJTP38RZ.C2Q\J3P4OJ0Y.VMC\epha..tion_4db49883e8ccc529_0001.0000_ad0f53dec1eea469\EPHARMA.POSWEB.PLUGIN.exe")
APPREF_PATH = os.getenv("APPREF_PATH", r"C:\Users\gabri\Desktop\ePharmaPlugin.appref-ms")
ICON_TOOLTIP = "epharma POS Web"
backend = "uia"  # ou backend, dependendo do que você preferir

def start_epharma():
    """
    Inicia a aplicação e-Pharma.
    """
    try:

        # Caminho para o atalho na sua área de trabalho (para iniciar)
        appref_path = APPREF_PATH
        # Inicia a aplicação usando o atalho
        os.startfile(appref_path)

        # ESPERA a aplicação carregar. Este passo é crucial!
        print("Aguardando 15 segundos para a aplicação carregar...")
        time.sleep(15)

        
    except Exception as e:
        print(f"Erro ao iniciar a aplicação e-Pharma: {e}")



def install_epharma():
    """
    Instala a aplicação e-Pharma.
    """
    try:
        app = Application(backend=backend).start("C:\\Users\\gabri\\Desktop\\Dassete\\setup.exe")
        app.wait_cpu_usage_lower(threshold=5, timeout=60)
        print("e-Pharma instalado com sucesso.")
        return app
    except Exception as e:
        print(f"Erro ao instalar a aplicação e-Pharma: {e}")

def get_epharma_app():
    """
    Obtém a instância da aplicação e-Pharma.
    Se a aplicação não estiver conectada, inicializa-a.
    """
    # Caminho REAL do executável (para conectar)
    real_exe_path = REAL_EXE_PATH
    app = None  # Inicializamos a variável como None para evitar o UnboundLocalError

    # --- Lógica de Inicialização e Conexão ---
    
    # 1. Tenta se conectar a um processo que já esteja rodando
    try:
        print("Tentando conectar a um processo existente...")
        app = Application(backend=backend).connect(path=real_exe_path, timeout=5)
        print("✅ Sucesso! Conectado a uma instância já em execução.")
        
       
    except ProcessNotFoundError:
        print("Nenhuma instância encontrada. Iniciando uma nova...")
    return app if app else None


def close_epharma(app=None):
    """
    Fecha a aplicação e-Pharma.
    """
    try:
        if not app:
            app = get_epharma_app()
        if app:
            app.kill()
    except Exception as e:
        print(f"Erro ao fechar a aplicação e-Pharma: {e}")


def initialize_epharma():
    """
    Inicializa a aplicação e-Pharma.
    Se a aplicação já estiver aberta, não faz nada.
    """
    close_epharma()  
    start_epharma()
    app = get_epharma_app()
    if not app:
        app = install_epharma()
        close_epharma(app)  
        start_epharma()
        app = get_epharma_app()
        if not app:
            raise RuntimeError("Não foi possível iniciar a aplicação e-Pharma.")
        
    else:
        print("A aplicação e-Pharma já está aberta.")


    return app if app else None