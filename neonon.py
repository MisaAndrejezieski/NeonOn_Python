"""
NEONON - Player de Midia Profissional
Versao Python com PyWebView
Desenvolvido por Misa
"""

import json
import logging
import os
import sys
from pathlib import Path

import webview

# ============================================
# CONFIGURACAO DE LOGGING (SEM EMOJIS)
# ============================================
log_dir = os.path.join(os.path.expanduser("~"), ".neonon", "logs")
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir + '/neonon.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("NeonOn")

# ============================================
# CONFIGURACOES DO APP
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
# GERENCIADOR DE CONFIGURACOES
# ============================================
def get_config_path():
    config_dir = os.path.join(os.path.expanduser("~"), ".neonon")
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, 'config.json')

# ============================================
# CLASSE API
# ============================================
class NeonOnAPI:
    def __init__(self):
        self.current_folder = None
        logger.info("API do NeonOn inicializada")
    
    # ============================================
    # LISTAR CONTEUDO DA PASTA (COM SEGURANCA)
    # ============================================
    def get_folder_contents(self, folder_path):
        try:
            # Validacao de seguranca
            if not os.path.exists(folder_path):
                return {'success': False, 'error': 'Pasta nao encontrada'}
            
            if not os.path.isdir(folder_path):
                return {'success': False, 'error': 'Caminho nao e uma pasta'}
            
            # Restricao ao diretorio base
            real_path = os.path.realpath(folder_path)
            base_real = os.path.realpath(BASE_PATH)
            
            if not real_path.startswith(base_real):
                return {'success': False, 'error': 'Acesso nao permitido a esta pasta'}
            
            # Listar arquivos
            video_ext = ['.mp4', '.webm', '.ogg', '.mov', '.avi', '.mkv', 
                        '.wmv', '.flv', '.m4v']
            image_ext = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.ico']
            
            files = []
            
            with os.scandir(folder_path) as entries:
                for entry in entries:
                    if entry.is_file():
                        ext = os.path.splitext(entry.name)[1].lower()
                        if ext in video_ext or ext in image_ext:
                            try:
                                stat = entry.stat()
                                files.append({
                                    'name': entry.name,
                                    'path': entry.path,
                                    'type': 'video' if ext in video_ext else 'image',
                                    'size': stat.st_size
                                })
                            except OSError:
                                pass
            
            files.sort(key=lambda x: x['name'].lower())
            
            logger.info(f"Listados {len(files)} arquivos em {folder_path}")
            return {'success': True, 'files': files}
            
        except PermissionError:
            return {'success': False, 'error': 'Permissao negada para acessar esta pasta'}
        except Exception as e:
            logger.error(f"Erro ao listar {folder_path}: {e}")
            return {'success': False, 'error': f'Erro ao listar arquivos: {str(e)}'}
    
    # ============================================
    # ABRIR DIALOGO PARA SELECIONAR PASTA (CORRIGIDO)
    # ============================================
    def open_folder_dialog(self):
        try:
            # PyWebView NAO aceita 'title' como parametro
            result = webview.windows[0].create_file_dialog(
                webview.FOLDER_DIALOG
                # O titulo e definido pelo sistema
            )
            if result:
                selected_path = result[0]
                logger.info(f"Pasta selecionada: {selected_path}")
                return selected_path
            logger.info("Selecao de pasta cancelada")
            return None
        except Exception as e:
            logger.error(f"Erro ao abrir dialogo de pasta: {e}")
            return None
    
    # ============================================
    # SALVAR PREFERENCIAS
    # ============================================
    def save_preferences(self, preferences):
        try:
            config_path = get_config_path()
            
            existing = {}
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    existing = json.load(f)
            
            existing.update(preferences)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(existing, f, indent=2)
            
            return {'success': True}
            
        except Exception as e:
            logger.error(f"Erro ao salvar preferencias: {e}")
            return {'success': False, 'error': str(e)}
    
    # ============================================
    # CARREGAR PREFERENCIAS
    # ============================================
    def load_preferences(self):
        try:
            config_path = get_config_path()
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Erro ao carregar preferencias: {e}")
            return {}

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
    logger.info("Janela principal criada")
    return window

# ============================================
# INICIALIZACAO
# ============================================
def main():
    logger.info("=" * 50)
    logger.info("INICIANDO NEONON PLAYER")
    logger.info(f"Caminho base: {BASE_PATH}")
    logger.info(f"Caminho web: {WEB_PATH}")
    logger.info(f"Configuracoes: {get_config_path()}")
    logger.info("=" * 50)
    
    if not os.path.exists(WEB_PATH):
        logger.error(f"Pasta WEB nao encontrada em: {WEB_PATH}")
        print(f"ERRO: Pasta 'web' nao encontrada em {WEB_PATH}")
        print("Certifique-se de que a pasta 'web' esta no mesmo diretorio que o executavel.")
        input("Pressione ENTER para sair...")
        sys.exit(1)
    
    window = create_window()
    webview.start(
        private_mode=False,
        debug=True,
        http_server=True
    )
    logger.info("Aplicativo finalizado")

if __name__ == '__main__':
    main()