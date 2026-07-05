"""
NEONON - Player de Mídia Profissional
Versão Python com PyWebView
Desenvolvido por Misa 💜
"""

import datetime
import json
import os
import sys
import time
from pathlib import Path

import webview

# --- IMPORTAÇÕES PARA WHATSAPP ---
try:
    import pywhatkit as kit
    WHATSAPP_AVAILABLE = True
except ImportError:
    WHATSAPP_AVAILABLE = False
    print('⚠️ pywhatkit não instalado. pip install pywhatkit')

# --- CONFIGURAÇÕES ---
APP_NAME = "NeonOn Player"
APP_WIDTH = 1200
APP_HEIGHT = 800
SEU_NUMERO = "42991378801"  # SEU NÚMERO COM DDD (SEM 55)

# --- OBTENDO CAMINHO BASE ---
def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

BASE_PATH = get_base_path()
WEB_PATH = os.path.join(BASE_PATH, 'web')
INDEX_PATH = os.path.join(WEB_PATH, 'index.html')

# --- API PYTHON PARA JAVASCRIPT ---
class NeonOnAPI:
    def __init__(self):
        self.current_folder = None
    
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
    
    def save_preferences(self, preferences):
        try:
            config_path = os.path.join(BASE_PATH, 'config.json')
            with open(config_path, 'w') as f:
                json.dump(preferences, f)
            return {'success': True}
        except Exception as e:
            return {'error': str(e)}
    
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
    # FUNÇÃO ENVIAR PARA WHATSAPP
    # ============================================
    def send_to_whatsapp(self, file_path, phone_number=None):
        """
        Envia arquivo para o WhatsApp do usuário
        Usa pywhatkit (abre WhatsApp Web e envia automaticamente)
        """
        try:
            if not WHATSAPP_AVAILABLE:
                return {'error': 'pywhatkit não instalado. Execute: pip install pywhatkit'}
            
            if not os.path.exists(file_path):
                return {'error': 'Arquivo não encontrado'}
            
            # Usa o número padrão se não for fornecido
            if not phone_number:
                phone_number = SEU_NUMERO
            
            # Formata o número
            phone = f"+55{phone_number}"
            file_name = os.path.basename(file_path)
            
            # Mensagem personalizada
            message = f"📹 NeonOn enviou:\n{file_name}\n\n💜 Desenvolvido por Misa"
            
            # Pega a hora atual + 2 minutos
            now = datetime.datetime.now()
            hour = now.hour
            minute = now.minute + 2
            
            if minute >= 60:
                minute -= 60
                hour += 1
            if hour >= 24:
                hour = 0
            
            print(f"📤 Enviando para {phone} às {hour:02d}:{minute:02d}")
            
            # Envia a mensagem
            kit.sendwhatmsg(phone, message, hour, minute)
            
            # Aguarda o envio
            time.sleep(10)
            
            # Tenta enviar o arquivo (se for imagem)
            if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                try:
                    kit.sendwhats_image(phone, file_path, caption="📸 Imagem enviada pelo NeonOn")
                    time.sleep(5)
                except:
                    pass
            
            return {
                'success': True,
                'message': f'Arquivo enviado para +55{phone_number}',
                'file': file_name
            }
            
        except Exception as e:
            return {'error': str(e)}

# --- CRIAÇÃO DA JANELA ---
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

# --- INICIALIZAÇÃO ---
def main():
    window = create_window()
    webview.start(
        private_mode=False,
        debug=True,
        http_server=True
    )

if __name__ == '__main__':
    main()