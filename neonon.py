"""
NEONON - Player de Mídia Profissional
Versão Python com PyWebView
Desenvolvido por Misa 💜
"""

import json
import os
import sys
from pathlib import Path

import webview

# --- CONFIGURAÇÕES ---
APP_NAME = "NeonOn Player"
APP_WIDTH = 1200
APP_HEIGHT = 800

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
        http_server=True,
        gui='cef'
    )

if __name__ == '__main__':
    main()