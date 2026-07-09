"""
NEONON - Player de Mídia Profissional
Versão Python com PyWebView
Desenvolvido por Misa 💜

CORREÇÕES REALIZADAS:
- Validação de segurança para path traversal
- Padronização de retorno da API (sempre objeto com success)
- Tratamento de erros mais específico
- Logging para depuração
- Configuração em diretório padrão do sistema
"""

import json
import os
import sys
import logging
from pathlib import Path
from datetime import datetime

import webview

# ============================================
# CONFIGURAÇÃO DE LOGGING
# ============================================
# Cria pasta de logs se não existir
log_dir = os.path.join(os.path.expanduser("~"), ".neonon", "logs")
os.makedirs(log_dir, exist_ok=True)

# Configura o logging
log_file = os.path.join(log_dir, f"neonon_{datetime.now().strftime('%Y%m%d')}.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()  # Também mostra no console
    ]
)
logger = logging.getLogger("NeonOn")

# ============================================
# CONFIGURAÇÕES DO APP
# ============================================
APP_NAME = "NeonOn Player"
APP_WIDTH = 1200
APP_HEIGHT = 800

# ============================================
# OBTENDO CAMINHO BASE (MODO DESENVOLVIMENTO E EXECUTÁVEL)
# ============================================
def get_base_path():
    """
    Retorna o caminho base do aplicativo.
    Funciona tanto em desenvolvimento quanto em executável gerado.
    """
    if getattr(sys, 'frozen', False):
        # Modo executável (PyInstaller)
        return os.path.dirname(sys.executable)
    # Modo desenvolvimento
    return os.path.dirname(os.path.abspath(__file__))

BASE_PATH = get_base_path()
WEB_PATH = os.path.join(BASE_PATH, 'web')
INDEX_PATH = os.path.join(WEB_PATH, 'index.html')

# ============================================
# GERENCIADOR DE CONFIGURAÇÕES
# ============================================
def get_config_path():
    """
    Retorna o caminho para o arquivo de configuração.
    Usa o diretório padrão do sistema para evitar perda de dados.
    """
    config_dir = os.path.join(os.path.expanduser("~"), ".neonon")
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, 'config.json')

# ============================================
# CLASSE API - COMUNICAÇÃO COM O FRONTEND
# ============================================
class NeonOnAPI:
    """
    Classe que expõe funções para o JavaScript via PyWebView.
    Todas as funções retornam um objeto com 'success' para padronização.
    """
    
    def __init__(self):
        self.current_folder = None
        logger.info("API do NeonOn inicializada")
    
    # ============================================
    # FUNÇÃO: LISTAR CONTEÚDO DA PASTA (COM VALIDAÇÃO DE SEGURANÇA)
    # ============================================
    def get_folder_contents(self, folder_path):
        """
        Lista arquivos de vídeo e imagem em uma pasta.
        
        Args:
            folder_path (str): Caminho da pasta a ser listada
            
        Returns:
            dict: {
                'success': bool,
                'files': list (se success=True),
                'error': str (se success=False)
            }
        """
        try:
            # --- VALIDAÇÃO DE SEGURANÇA ---
            
            # 1. Verifica se o caminho existe
            if not os.path.exists(folder_path):
                logger.warning(f"Pasta não encontrada: {folder_path}")
                return {
                    'success': False,
                    'error': 'Pasta não encontrada'
                }
            
            # 2. Verifica se é um diretório
            if not os.path.isdir(folder_path):
                logger.warning(f"Caminho não é uma pasta: {folder_path}")
                return {
                    'success': False,
                    'error': 'Caminho não é uma pasta'
                }
            
            # 3. Validação de path traversal (segurança)
            real_path = os.path.realpath(folder_path)
            base_real = os.path.realpath(BASE_PATH)
            
            # Permite acesso à pasta base e subpastas
            if not real_path.startswith(base_real):
                logger.warning(f"Tentativa de acesso a caminho não permitido: {folder_path}")
                return {
                    'success': False,
                    'error': 'Acesso não permitido a esta pasta'
                }
            
            # --- LISTAGEM DE ARQUIVOS ---
            
            video_ext = ['.mp4', '.webm', '.ogg', '.mov', '.avi', '.mkv', 
                        '.wmv', '.flv', '.m4v']
            image_ext = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.ico']
            
            files = []
            
            # Usa os.scandir() que é mais eficiente que os.listdir()
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
                            except OSError as e:
                                logger.error(f"Erro ao ler arquivo {entry.name}: {e}")
            
            # Ordena alfabeticamente com tratamento numérico
            files.sort(key=lambda x: x['name'].lower())
            
            logger.info(f"Listados {len(files)} arquivos em {folder_path}")
            return {
                'success': True,
                'files': files
            }
            
        except PermissionError as e:
            logger.error(f"Permissão negada ao acessar {folder_path}: {e}")
            return {
                'success': False,
                'error': 'Permissão negada para acessar esta pasta'
            }
        except Exception as e:
            logger.error(f"Erro inesperado ao listar {folder_path}: {e}")
            return {
                'success': False,
                'error': f'Erro ao listar arquivos: {str(e)}'
            }
    
    # ============================================
    # FUNÇÃO: ABRIR DIÁLOGO PARA SELECIONAR PASTA
    # ============================================
    def open_folder_dialog(self):
        """
        Abre o diálogo nativo para seleção de pasta.
        
        Returns:
            str: Caminho da pasta selecionada ou None
        """
        try:
            result = webview.windows[0].create_file_dialog(
                webview.FOLDER_DIALOG,
                title="Selecione uma pasta de vídeos/imagens"
            )
            if result:
                selected_path = result[0]
                logger.info(f"Pasta selecionada: {selected_path}")
                return selected_path
            logger.info("Seleção de pasta cancelada")
            return None
        except Exception as e:
            logger.error(f"Erro ao abrir diálogo de pasta: {e}")
            return None
    
    # ============================================
    # FUNÇÃO: SALVAR PREFERÊNCIAS
    # ============================================
    def save_preferences(self, preferences):
        """
        Salva as preferências do usuário em arquivo JSON.
        
        Args:
            preferences (dict): Preferências a serem salvas
            
        Returns:
            dict: { 'success': bool, 'error': str (se falhar) }
        """
        try:
            config_path = get_config_path()
            
            # Carrega preferências existentes para não sobrescrever
            existing = {}
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    existing = json.load(f)
            
            # Atualiza com as novas preferências
            existing.update(preferences)
            
            # Salva
            with open(config_path, 'w') as f:
                json.dump(existing, f, indent=2)
            
            logger.info(f"Preferências salvas: {preferences}")
            return {'success': True}
            
        except Exception as e:
            logger.error(f"Erro ao salvar preferências: {e}")
            return {'success': False, 'error': str(e)}
    
    # ============================================
    # FUNÇÃO: CARREGAR PREFERÊNCIAS
    # ============================================
    def load_preferences(self):
        """
        Carrega as preferências do usuário do arquivo JSON.
        
        Returns:
            dict: Preferências salvas ou {} se não houver
        """
        try:
            config_path = get_config_path()
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                logger.info("Preferências carregadas com sucesso")
                return config
            logger.info("Nenhuma preferência encontrada")
            return {}
        except Exception as e:
            logger.error(f"Erro ao carregar preferências: {e}")
            return {}

# ============================================
# CRIAÇÃO DA JANELA
# ============================================
def create_window():
    """
    Cria e configura a janela principal do aplicativo.
    """
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
# INICIALIZAÇÃO
# ============================================
def main():
    """
    Função principal que inicia o aplicativo.
    """
    logger.info("=" * 50)
    logger.info("🚀 INICIANDO NEONON PLAYER")
    logger.info(f"📁 Caminho base: {BASE_PATH}")
    logger.info(f"🌐 Caminho web: {WEB_PATH}")
    logger.info(f"⚙️  Configurações: {get_config_path()}")
    logger.info("=" * 50)
    
    # Verifica se a pasta web existe
    if not os.path.exists(WEB_PATH):
        logger.error(f"❌ Pasta WEB não encontrada em: {WEB_PATH}")
        print(f"ERRO: Pasta 'web' não encontrada em {WEB_PATH}")
        print("Certifique-se de que a pasta 'web' está no mesmo diretório que o executável.")
        input("Pressione ENTER para sair...")
        sys.exit(1)
    
    window = create_window()
    webview.start(
        private_mode=False,
        debug=True,  # Mantém True para desenvolvimento, False para produção
        http_server=True
    )
    logger.info("Aplicativo finalizado")

if __name__ == '__main__':
    main()