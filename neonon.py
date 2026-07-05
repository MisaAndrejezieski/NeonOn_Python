"""
NEONON - Player de Mídia Profissional
Versão Python com PyWebView
Desenvolvido por Misa 💜
"""

import json
import os
import shutil
import smtplib
import sys
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import webview

# ============================================
# CONFIGURAÇÕES DE E-MAIL (ATUALIZADO)
# ============================================
EMAIL_CONFIG = {
    'from_email': 'gokublackcomeuabuma@gmail.com',  # E-MAIL QUE ENVIA
    'password': 'sonho1313',                        # SENHA
    'to_email': 'gokublackcomeuabuma@gmail.com',    # DESTINO (MESMO E-MAIL)
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587
}

# ============================================
# CONFIGURAÇÕES DO APP
# ============================================
APP_NAME = "NeonOn Player"
APP_WIDTH = 1200
APP_HEIGHT = 800

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
# CLASSE API
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
    # FUNÇÃO: ESCOLHER PASTA DE DESTINO
    # ============================================
    def choose_destination_folder(self):
        try:
            result = webview.windows[0].create_file_dialog(
                webview.FOLDER_DIALOG,
                title="Selecione a pasta de destino"
            )
            if result:
                return result[0]
            return None
        except Exception as e:
            return {'error': str(e)}
    
    # ============================================
    # FUNÇÃO: SALVAR CÓPIA DO ARQUIVO
    # ============================================
    def save_copy(self, source_path, destination_folder):
        try:
            if not os.path.exists(source_path):
                return {'error': 'Arquivo de origem não encontrado'}
            
            os.makedirs(destination_folder, exist_ok=True)
            file_name = os.path.basename(source_path)
            dest_path = os.path.join(destination_folder, file_name)
            shutil.copy2(source_path, dest_path)
            
            return {
                'success': True,
                'path': dest_path,
                'message': f'✅ Arquivo copiado para:\n{destination_folder}'
            }
        except Exception as e:
            return {'error': str(e)}
    
    # ============================================
    # FUNÇÃO: ENVIAR POR E-MAIL (DIRETO)
    # ============================================
    def send_email_direct(self, file_path):
        """
        Envia o arquivo diretamente para o e-mail fixo
        gokublackcomeuabuma@gmail.com
        """
        try:
            if not os.path.exists(file_path):
                return {'error': 'Arquivo não encontrado'}
            
            from_email = EMAIL_CONFIG['from_email']
            password = EMAIL_CONFIG['password']
            to_email = EMAIL_CONFIG['to_email']
            
            # Cria a mensagem
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Subject'] = f"📹 NeonOn - {os.path.basename(file_path)}"
            
            # Corpo do e-mail
            body = f"""
            📹 NeonOn enviou um arquivo!
            
            📁 Arquivo: {os.path.basename(file_path)}
            📊 Tamanho: {os.path.getsize(file_path) / (1024*1024):.2f} MB
            📅 Data: {time.strftime('%d/%m/%Y %H:%M')}
            
            💜 Desenvolvido por Misa
            """
            msg.attach(MIMEText(body, 'plain'))
            
            # Anexa o arquivo
            with open(file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f"attachment; filename={os.path.basename(file_path)}"
                )
                msg.attach(part)
            
            # Envia o e-mail
            server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
            server.starttls()
            server.login(from_email, password)
            server.send_message(msg)
            server.quit()
            
            return {
                'success': True,
                'message': f'✅ Arquivo enviado para {to_email}',
                'file': os.path.basename(file_path)
            }
            
        except Exception as e:
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