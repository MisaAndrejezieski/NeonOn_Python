"""
NEONON - Player de Mídia Profissional
Versão Python com PyWebView
Desenvolvido por Misa 💜
"""

import json
import os
import sys
import time
from pathlib import Path

import webview

# ============================================
# IMPORTAÇÕES PARA WHATSAPP (SELENIUM)
# ============================================
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print('⚠️ Selenium não instalado. Execute: pip install selenium webdriver-manager')

# ============================================
# CONFIGURAÇÕES
# ============================================
APP_NAME = "NeonOn Player"
APP_WIDTH = 1200
APP_HEIGHT = 800
SEU_NUMERO = "42991378801"  # SEU NÚMERO COM DDD (SEM 55)

# ============================================
# OBTENDO CAMINHO BASE
# ============================================
def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

BASE_PATH = get_base_path()
WEB_PATH = os.path.join(BASE_PATH, 'web')
INDEX_PATH = os.path.join(WEB_PATH, 'index.html')

# ============================================
# CLASSE API - COMUNICAÇÃO PYTHON ↔ JAVASCRIPT
# ============================================
class NeonOnAPI:
    def __init__(self):
        self.current_folder = None
    
    # ============================================
    # FUNÇÃO: LISTAR CONTEÚDO DA PASTA
    # ============================================
    def get_folder_contents(self, folder_path):
        try:
            video_ext = ['.mp4', '.webm', '.ogg', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.m4v']
            image_ext = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.ico']
            
            files = []
            for file in os.listdir(folder_path):
                ext = os.path.splitext(file)[1].lower()
                if ext in video_ext or ext in image_ext:
                    full_path = os.path.join(folder_path, file)
                    files.append({
                        'name': file,
                        'path': full_path,
                        'type': 'video' if ext in video_ext else 'image',
                        'size': os.path.getsize(full_path)
                    })
            files.sort(key=lambda x: x['name'].lower())
            return files
        except Exception as e:
            return {'error': str(e)}
    
    # ============================================
    # FUNÇÃO: ABRIR DIÁLOGO PARA SELECIONAR PASTA
    # ============================================
    def open_folder_dialog(self):
        try:
            result = webview.windows[0].create_file_dialog(
                webview.FOLDER_DIALOG,
                title="Selecione uma pasta de vídeos/imagens"
            )
            if result:
                return result[0]
            return None
        except Exception as e:
            return {'error': str(e)}
    
    # ============================================
    # FUNÇÃO: SALVAR PREFERÊNCIAS
    # ============================================
    def save_preferences(self, preferences):
        try:
            config_path = os.path.join(BASE_PATH, 'config.json')
            with open(config_path, 'w') as f:
                json.dump(preferences, f)
            return {'success': True}
        except Exception as e:
            return {'error': str(e)}
    
    # ============================================
    # FUNÇÃO: CARREGAR PREFERÊNCIAS
    # ============================================
    def load_preferences(self):
        try:
            config_path = os.path.join(BASE_PATH, 'config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    return json.load(f)
            return {}
        except Exception:
            return {}
    
    # ============================================
    # FUNÇÃO: ENVIAR PARA WHATSAPP (SELENIUM)
    # ============================================
    def send_to_whatsapp(self, file_path, phone_number=None):
        """
        Envia arquivo para o WhatsApp usando Selenium
        FUNCIONA PARA VÍDEOS E IMAGENS!
        100% automático após escanear o QR Code
        """
        try:
            if not SELENIUM_AVAILABLE:
                return {'error': 'Selenium não instalado. Execute: pip install selenium webdriver-manager'}
            
            if not os.path.exists(file_path):
                return {'error': 'Arquivo não encontrado'}
            
            # Usa o número padrão se não for fornecido
            if not phone_number:
                phone_number = SEU_NUMERO
            
            print(f"📤 Enviando arquivo para +55{phone_number}...")
            print(f"📁 Arquivo: {os.path.basename(file_path)}")
            
            # ============================================
            # CONFIGURA O CHROME
            # ============================================
            options = Options()
            options.add_argument('--user-data-dir=./whatsapp_session')  # Mantém login
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            options.add_experimental_option('useAutomationExtension', False)
            
            # ============================================
            # INICIA O DRIVER
            # ============================================
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )
            
            # ============================================
            # ABRE O WHATSAPP WEB
            # ============================================
            driver.get("https://web.whatsapp.com")
            
            # Espera o login (60 segundos para escanear o QR Code)
            wait = WebDriverWait(driver, 60)
            wait.until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"]')))
            
            # ============================================
            # ABRE O CHAT COM O NÚMERO
            # ============================================
            phone = f"55{phone_number}"
            chat_url = f"https://web.whatsapp.com/send?phone={phone}"
            driver.get(chat_url)
            time.sleep(3)
            
            # ============================================
            # 1. CLICA NO BOTÃO DE ANEXAR
            # ============================================
            attach_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@title="Anexar"]')))
            attach_btn.click()
            time.sleep(1)
            
            # ============================================
            # 2. SELECIONA A OPÇÃO "DOCUMENTO"
            # ============================================
            file_input = driver.find_element(By.XPATH, '//input[@accept="*"]')
            file_input.send_keys(os.path.abspath(file_path))
            time.sleep(3)  # Espera o upload
            
            # ============================================
            # 3. DIGITA A MENSAGEM
            # ============================================
            message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@spellcheck="true"]')
            file_name = os.path.basename(file_path)
            message = f"📹 NeonOn enviou:\n{file_name}\n\n💜 Desenvolvido por Misa"
            message_box.send_keys(message)
            
            # ============================================
            # 4. CLICA EM ENVIAR
            # ============================================
            send_btn = driver.find_element(By.XPATH, '//span[@data-icon="send"]')
            send_btn.click()
            
            # Aguarda o envio
            time.sleep(5)
            
            # ============================================
            # FECHA O NAVEGADOR
            # ============================================
            driver.quit()
            
            print("✅ Arquivo enviado com sucesso!")
            
            return {
                'success': True,
                'message': f'✅ Arquivo enviado para +55{phone_number}',
                'file': file_name
            }
            
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
            return {'error': str(e)}

# ============================================
# CRIAÇÃO DA JANELA
# ============================================
def create_window():
    api = NeonOnAPI()
    window = webview.create_window(
        APP_NAME,
        INDEX_PATH,
        width=APP_WIDTH,
        height=APP_HEIGHT,
        resizable=True,
        fullscreen=False,
        min_size=(800, 600),
        text_select=True,
        confirm_close=True,
        js_api=api,
        background_color='#0a0a14'
    )
    return window

# ============================================
# INICIALIZAÇÃO
# ============================================
def main():
    window = create_window()
    webview.start(
        private_mode=False,
        debug=True,
        http_server=True
    )

if __name__ == '__main__':
    main()