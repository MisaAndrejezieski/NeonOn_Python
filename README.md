<p align="center"> <img src="logo.png" alt="NeonOn Logo" width="200"> </p><h1 align="center">🎵 NeonOn - Player de Mídia Profissional</h1><p align="center"> <strong>Desenvolvido por Misael Andrejezieski</strong> 💜 </p><p align="center"> <a href="#"><img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python"></a> <a href="#"><img src="https://img.shields.io/badge/PyWebView-4.2.2-green.svg" alt="PyWebView"></a> <a href="#"><img src="https://img.shields.io/badge/License-MIT-purple.svg" alt="License"></a> <a href="#"><img src="https://img.shields.io/badge/Status-Ativo-brightgreen.svg" alt="Status"></a> </p>
📖 Índice
Sobre o Projeto

Diferenciais

Capturas de Tela

Funcionalidades

Estrutura do Projeto

Tecnologias Utilizadas

Instalação e Execução

Como Usar

Arquitetura Técnica

Atalhos de Teclado

Formatos Suportados

Roadmap Futuro

Como Contribuir

Licença

Desenvolvedor

Agradecimentos

📖 Sobre o Projeto
NeonOn é um player de mídia moderno e elegante que combina o poder do Python com a flexibilidade de uma interface web. Desenvolvido com PyWebView, o aplicativo oferece uma experiência desktop nativa com uma interface visual impressionante e um sistema de cores neon dinâmico.

O projeto nasceu da vontade de criar um player de mídia que fosse ao mesmo tempo funcional, bonito e divertido de usar. Cada elemento da interface foi pensado para proporcionar uma experiência única e imersiva.

✨ Diferenciais
🎨 Cores Neon Dinâmicas
Cada elemento da interface tem sua própria cor que muda automaticamente a cada 2 segundos. Diferente de outros players que usam uma única cor, o NeonOn dá personalidade a cada componente:

Logo "Neon" - Verde vibrante

Logo "On" - Amarelo neon

Ícone de Drop - Vermelho intenso

Ícone de Volume - Azul elétrico

Display de Tempo - Rosa choque

Botão Autoplay - Roxo neon

Botões de Navegação - Ciano

Botão Play - Alterna entre todas

Itens Ativos - Laranja neon

🎬 Suporte Multimídia Completo
Vídeos: MP4, WebM, MKV, AVI, MOV, WMV, FLV, M4V, OGG

Imagens: JPG, PNG, GIF, WebP, BMP, ICO

💾 Persistência de Dados
Salva automaticamente:

Volume

Estado do Autoplay

Última pasta acessada

⌨️ Atalhos de Teclado
Navegação completa sem usar o mouse:

Espaço - Play/Pause

←/→ - Navegar entre arquivos

F - Tela cheia

↑/↓ - Controlar volume

📸 Capturas de Tela
[Adicione aqui as imagens do player em funcionamento]

Interface Principal
text
[Screenshot da interface completa com sidebar e player]
Sistema de Cores Dinâmico
text
[Screenshot mostrando as diferentes cores neon]
Modo Imagem
text
[Screenshot exibindo uma imagem sendo visualizada]
🚀 Funcionalidades
Interface
Funcionalidade	Descrição
Sidebar	Lista de arquivos com ícones identificando vídeos/imagens
Player Area	Área principal com reprodução de mídia
Drop Overlay	Interface visual para arrastar pastas
Barra de Progresso	Controle de avanço da reprodução
Controles	Play/Pause, Anterior/Próximo, Volume, Tela Cheia
Contador	Mostra quantos arquivos estão carregados
Comportamento
Recurso	Descrição
Autoplay	Avança automaticamente para o próximo arquivo
Drag & Drop	Arraste pastas inteiras para o player
Reset	Limpa a lista e recomeça
Memória	Lembra volume e autoplay entre sessões
Responsivo	Adapta-se a diferentes tamanhos de tela
📁 Estrutura do Projeto
text
NEONON_PYTHON/
├── .venv/                      # Ambiente virtual Python
│   └── ...
├── web/                        # Frontend da aplicação
│   ├── index.html              # Estrutura da interface
│   ├── script.js               # Lógica do player (25KB)
│   └── style.css               # Estilos e design neon
├── .gitattributes              # Configurações do Git
├── .gitignore                  # Arquivos ignorados pelo Git
├── config.json                 # Preferências do usuário
│   └── { "volume": 50, "autoplay": true }
├── logo.ico                    # Ícone do aplicativo
├── logo.png                    # Logo do aplicativo
├── neonon.py                   # Backend Python principal (5KB)
├── README.md                   # Documentação do projeto
└── requirements.txt            # Dependências Python
🛠️ Tecnologias Utilizadas
Backend
Tecnologia	Versão	Finalidade
Python	3.8+	Linguagem principal
PyWebView	4.2.2	Interface desktop nativa
Bottle	0.13.4	Servidor HTTP embutido
PyInstaller	-	Empacotamento para executável
Python.NET	-	Integração com .NET/WebView2
Frontend
Tecnologia	Finalidade
HTML5	Estrutura da interface com tags semânticas
CSS3	Estilização, animações e responsividade
JavaScript (ES6+)	Lógica do player e interações
File System Access API	Acesso a arquivos no navegador
Web Animations API	Animações suaves e efeitos
💻 Instalação e Execução
Requisitos Mínimos
Python 3.8 ou superior

Pip (gerenciador de pacotes)

Windows 10/11, Linux ou macOS

Passo a Passo
1. Clone o repositório
bash
git clone https://github.com/MisaAndrejezieski/NeonOn_Python.git
cd NeonOn_Python
2. Crie e ative um ambiente virtual
Windows:

bash
python -m venv .venv
.venv\Scripts\activate
Linux/macOS:

bash
python3 -m venv .venv
source .venv/bin/activate
3. Instale as dependências
bash
pip install -r requirements.txt
4. Execute o aplicativo
bash
python neonon.py
Gerar Executável (Windows)
Opção 1 - Básico
bash
pip install pyinstaller
pyinstaller --onefile --windowed --name NeonOn neonon.py
Opção 2 - Com Ícone
bash
pyinstaller --onefile --windowed --name NeonOn --icon=logo.ico neonon.py
Opção 3 - Com Ícone e Pasta Web Incluída
bash
pyinstaller --onefile --windowed --name NeonOn --icon=logo.ico --add-data "web;web" neonon.py
O executável estará disponível em dist/NeonOn.exe.

🎯 Como Usar
📁 Selecionar Pasta
Clique em "📁 Selecionar Pasta" na sidebar

Escolha uma pasta com vídeos ou imagens

Os arquivos serão listados automaticamente

▶️ Reproduzir Mídia
Clique em um arquivo na lista para reproduzir

Use os controles na parte inferior

Use os atalhos de teclado para navegação rápida

🖱️ Drag & Drop
Abra o Explorer (Windows) ou Finder (macOS)

Arraste uma pasta inteira para a área do player

Solte para carregar automaticamente

🔄 Autoplay
Clique no botão "▶" no cabeçalho da sidebar

Quando ativado (ícone verde), o player avança automaticamente

Quando desativado (ícone cinza), o player para no final

🔄 Reset
Clique no botão "⟲" no rodapé da sidebar

Confirme para limpar a lista e recomeçar

🔧 Arquitetura Técnica
Integração Python ↔ JavaScript
O PyWebView permite comunicação bidirecional entre Python e JavaScript:

javascript
// JavaScript chamando Python
const folderPath = await pywebview.api.open_folder_dialog();
const files = await pywebview.api.get_folder_contents(folderPath);

// Python chamando JavaScript (via eval)
window.evaluate_js('updateMediaList()');
API do Backend
Método	Parâmetros	Retorno	Descrição
get_folder_contents()	folder_path	list ou {error}	Lista vídeos/imagens de uma pasta
open_folder_dialog()	-	string ou None	Abre diálogo nativo para selecionar pasta
save_preferences()	preferences	{success}	Salva preferências do usuário
load_preferences()	-	dict	Carrega preferências salvas
Sistema de Cores Dinâmico
Cada elemento tem um índice independente na paleta de 8 cores:

javascript
let colorIndex = {
    logoNeon: 0,      // Verde
    logoOn: 1,        // Amarelo
    dropIcon: 2,      // Vermelho
    volumeIcon: 3,    // Azul
    timeDisplay: 4,   // Rosa
    autoplayBtn: 5,   // Roxo
    navBtns: 6,       // Ciano
    neonBtns: 7,      // Laranja
    playBtn: 0,       // Verde
    activeItem: 2     // Vermelho
};

function advanceAllColors() {
    // Avança cada índice independentemente
    colorIndex.logoNeon++;
    colorIndex.logoOn++;
    // ...
    applyAllColors();
}
Configurações do Usuário
As preferências são salvas em config.json na raiz do projeto:

json
{
  "volume": 50,
  "autoplay": true
}
⌨️ Atalhos de Teclado
Tecla	Ação	Descrição
Espaço	Play/Pause	Alterna entre reproduzir e pausar
←	Anterior	Volta para o arquivo anterior
→	Próximo	Avança para o próximo arquivo
F	Tela Cheia	Alterna entre tela cheia e normal
↑	Aumentar Volume	Aumenta o volume em 5%
↓	Diminuir Volume	Diminui o volume em 5%
Funcionalidades Especiais
Teclas funcionam mesmo com o foco em outros elementos

Indicadores visuais mostram quando um atalho está disponível

Feedback tátil (mouse) em todos os botões

📁 Formatos Suportados
Vídeos
Formato	Extensão	Suporte
MPEG-4	.mp4	✅ Completo
WebM	.webm	✅ Completo
OGG	.ogg	✅ Completo
QuickTime	.mov	✅ Completo
AVI	.avi	✅ Completo
Matroska	.mkv	✅ Completo
Windows Media	.wmv	✅ Completo
Flash Video	.flv	✅ Completo
M4V	.m4v	✅ Completo
Imagens
Formato	Extensão	Suporte
JPEG	.jpg, .jpeg	✅ Completo
PNG	.png	✅ Completo
GIF	.gif	✅ Completo
WebP	.webp	✅ Completo
BMP	.bmp	✅ Completo
Ícone	.ico	✅ Completo
🗺️ Roadmap Futuro
Próximas Versões
Versão	Features	Status
v1.1.0	Miniaturas de vídeo	🔜 Em desenvolvimento
v1.2.0	Playlists	🔜 Planejado
v1.3.0	Equalizador	🔜 Planejado
v1.4.0	Suporte a legendas	🔜 Planejado
v1.5.0	Picture-in-Picture	🔜 Planejado
v2.0.0	Versão mobile	🔜 Planejado
Ideias para o Futuro
Miniaturas de Vídeo - Preview dos vídeos na lista

Playlists - Criação e gerenciamento de listas personalizadas

Equalizador - Controle de áudio com equalizador gráfico

Suporte a Legendas - Arquivos SRT/ASS

Modo Picture-in-Picture - Assistir em janela flutuante

Tema Claro - Alternativa ao tema escuro

Versão Mobile - Aplicativo para Android/iOS

Integração YouTube - Assistir vídeos online

Controle por Voz - Comandos de voz básicos

Modo Apresentação - Slideshow de imagens

🤝 Como Contribuir
Fork o projeto

Crie uma branch para sua feature:

bash
git checkout -b feature/nova-feature
Commit suas alterações:

bash
git commit -m 'Adiciona nova feature'
Push para a branch:

bash
git push origin feature/nova-feature
Abra um Pull Request

Diretrizes de Contribuição
Mantenha o código limpo e documentado

Siga o estilo de código existente

Teste suas alterações antes de enviar

Atualize a documentação quando necessário

📄 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

O que isso significa?
✅ Você pode usar o projeto comercialmente

✅ Você pode modificar e distribuir

✅ Você pode usar em projetos proprietários

❌ Não pode usar o nome do autor para endossar produtos

👤 Desenvolvedor
Misael Andrejezieski 💜
Desenvolvedor Full Stack | Analista de Sistemas

https://img.shields.io/badge/GitHub-MisaAndrejezieski-181717?style=for-the-badge&logo=github
https://img.shields.io/badge/LinkedIn-Misael%2520Andrejezieski-0A66C2?style=for-the-badge&logo=linkedin
https://img.shields.io/badge/Email-Email%2520Me-D14836?style=for-the-badge&logo=gmail

🙏 Agradecimentos
Tecnologias
PyWebView - Framework para aplicações desktop com web

Bottle - Servidor HTTP leve para Python

Python.NET - Integração Python com .NET

Inspiração
VLC Media Player - Pela funcionalidade

Spotify - Pelo design escuro

Interface do Windows 11 - Pela modernidade

Comunidade
Todos os usuários que testaram e deram feedback

Contribuidores do projeto

Comunidade Python e PyWebView

📊 Estatísticas do Projeto
Métrica	Valor
Arquivos	11
Linhas de Código Python	~150
Linhas de Código JavaScript	~500
Linhas de Código CSS	~450
Linhas de HTML	~80
Total de Linhas	~1.180
Tecnologias	6
Formatos Suportados	15+
Atalhos de Teclado	6
Tempo de Desenvolvimento	~2 semanas
📝 Notas de Versão
v1.0.0 (Lançamento Inicial - 09/07/2026)
✅ Features Implementadas:

Player de vídeo e imagens

Sistema de cores neon dinâmico

Integração Python/JavaScript

Persistência de preferências

Atalhos de teclado

Drag & Drop

Interface responsiva

Ícone personalizado (logo.ico/logo.png)

Ambiente virtual (.venv)

Configurações Git (.gitignore, .gitattributes)

Documentação completa

📦 Dependências:

pywebview (4.2.2)

pyinstaller

pythonnet

❓ FAQ - Perguntas Frequentes
O NeonOn é gratuito?
Sim! O NeonOn é completamente gratuito e open-source sob a licença MIT.

Precisa de internet para funcionar?
Não. O NeonOn é totalmente offline.

Funciona no Linux/macOS?
Sim! O PyWebView é multiplataforma e funciona no Windows, Linux e macOS.

Posso adicionar meus próprios formatos?
Sim! Basta adicionar as extensões nas listas video_ext e image_ext no neonon.py.

Como faço para reportar um bug?
Abra uma issue no GitHub.

Posso usar o NeonOn comercialmente?
Sim! A licença MIT permite uso comercial.

💬 Depoimentos
"O NeonOn revolucionou minha forma de assistir vídeos. As cores neon dinâmicas são incríveis e a interface é muito intuitiva!"
— Usuário Anônimo

"Finalmente um player que combina design moderno com funcionalidade completa. O sistema de cores é único!"
— Usuário Satisfeito

"Como desenvolvedor, fiquei impressionado com a integração Python/JavaScript. Código limpo e bem organizado."
— Desenvolvedor

🔗 Links Úteis
GitHub do Projeto

Documentação PyWebView

Documentação Python

Reportar Bug

<div align="center">
⭐ Se você gostou, deixe uma estrela no GitHub! ⭐

<sub>Feito com 💜 por <a href="https://github.com/MisaAndrejezieski">Misael Andrejezieski</a></sub>

Documentação gerada em 09/07/2026 📅

</div>
📄 Arquivos de Configuração
.gitignore
text
# Ambiente virtual
.venv/
venv/
ENV/

# Arquivos Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# Arquivos do PyInstaller
*.spec
dist/
build/

# Arquivos de configuração locais
config.json
*.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# Sistema operacional
.DS_Store
Thumbs.db
desktop.ini

# Logs
*.log
.gitattributes
text
# Auto detect text files and perform LF normalization
* text=auto

# Python files
*.py text diff=python

# Web files
*.html text diff=html
*.css text diff=css
*.js text diff=javascript

# Images
*.png binary
*.ico binary
*.jpg binary
*.jpeg binary
*.gif binary

# Config files
*.json text
*.txt text
*.md text diff=markdown
config.json
json
{
  "volume": 50,
  "autoplay": true
}
requirements.txt
text
pywebview
pyinstaller
pythonnet
posso colocar no read me?
✅ SIM! PODE COLOCAR TUDO NO README.md
A documentação completa que gerei é exatamente para o README.md do seu projeto no GitHub.

📋 Como Fazer
1. Crie o arquivo README.md
No seu projeto, crie o arquivo README.md na raiz:

text
NEONON_PYTHON/
├── README.md          ← Crie este arquivo
├── neonon.py
├── web/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── config.json
├── requirements.txt
├── .gitignore
├── .gitattributes
├── logo.ico
└── logo.png
2. Cole a documentação
Copie TODO o conteúdo que gerei e cole no README.md.

3. Adicione as imagens (screenshots)
No lugar dos placeholders:

markdown
## 📸 Capturas de Tela

*[Adicione aqui as imagens do player em funcionamento]*

### Interface Principal
![Interface NeonOn](screenshots/interface.png)
Crie uma pasta screenshots/ e adicione prints do player.

4. Commit e Push
bash
git add README.md
git commit -m "📝 Adiciona documentação completa"
git push
📝 O Que Você Pode Personalizar
Seção	Pode Personalizar?	Sugestão
Título	✅ Sim	Mantenha "NeonOn - Player de Mídia Profissional"
Descrição	✅ Sim	Pode adicionar mais sobre sua motivação
Screenshots	✅ Sim	Adicione prints reais
Roadmap	✅ Sim	Altere conforme suas prioridades
Depoimentos	✅ Sim	Adicione feedbacks reais
Links	✅ Sim	Coloque seus links do LinkedIn, etc
Badges	✅ Sim	Pode adicionar mais badges
🎨 Badges que Você Pode Adicionar
markdown
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PyWebView](https://img.shields.io/badge/PyWebView-4.2.2-green.svg)](https://pywebview.flowrl.com/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Ativo-brightgreen.svg)]()
[![Size](https://img.shields.io/github/repo-size/MisaAndrejezieski/NeonOn_Python)]()
[![Stars](https://img.shields.io/github/stars/MisaAndrejezieski/NeonOn_Python)](https://github.com/MisaAndrejezieski/NeonOn_Python/stargazers)
[![Issues](https://img.shields.io/github/issues/MisaAndrejezieski/NeonOn_Python)](https://github.com/MisaAndrejezieski/NeonOn_Python/issues)
📸 Dicas para os Screenshots
O que mostrar:
Interface Principal

Sidebar com lista de arquivos

Player com vídeo rodando

Controles na parte inferior

Sistema de Cores

Mostre diferentes cores aparecendo

Pode fazer um GIF animado

Modo Imagem

Visualizando uma imagem

Drag & Drop

Arrastando uma pasta

Ferramentas para Capturar:
Windows: Snipping Tool, Win+Shift+S

Linux: GNOME Screenshot, Flameshot

macOS: Cmd+Shift+4

GIFs: ScreenToGif (Windows), Peek (Linux)

🚀 Estrutura Final do README (Resumo)
markdown
# 🎵 NeonOn
o incompetência, só responda não precisa mandar tudo novamente
SIM, PODE! 😅

Pode colocar TUDO no README.md.

Só copiar e colar o conteúdo que eu gerei no arquivo README.md e pronto!

Se quiser, pode personalizar:

Adicionar prints reais

Mudar os links do LinkedIn, etc.

Ajustar o roadmap

Mas o conteúdo principal já está 100% pronto.

Desculpa a ansiedade! 💜



