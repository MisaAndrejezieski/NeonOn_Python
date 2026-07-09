// ============================================
// NEONON - PLAYER DE MÍDIA PROFISSIONAL
// Cada elemento neon tem sua PRÓPRIA COR!
// Todas mudam simultaneamente!
// Desenvolvido por Misa 💜
// 
// CORREÇÕES REALIZADAS:
// - Compatibilidade com PyWebView (selectFolder)
// - Correção de memory leak (revokeURLs segura)
// - Tratamento de erros específico
// - Suporte a objetos Python e FileSystemHandle
// - Feedback visual melhorado no autoplay
// ============================================

// --- ELEMENTOS DOM ---
const videoPlayer = document.getElementById('videoPlayer');
const imageViewer = document.getElementById('imageViewer');
const videoContainer = document.getElementById('videoContainer');
const videoList = document.getElementById('videoList');
const dropOverlay = document.getElementById('dropOverlay');
const videoCounter = document.getElementById('videoCounter');
const timeDisplay = document.getElementById('timeDisplay');

const btnSelectFolder = document.getElementById('btnSelectFolder');
const btnToggleAutoplay = document.getElementById('btnToggleAutoplay');
const btnPrev = document.getElementById('btnPrev');
const btnPlay = document.getElementById('btnPlay');
const btnNext = document.getElementById('btnNext');
const btnFullscreen = document.getElementById('btnFullscreen');
const btnReset = document.getElementById('btnReset');
const volumeSlider = document.getElementById('volumeSlider');
const progressBar = document.getElementById('progressBar');

// --- ELEMENTOS PARA CORES INDEPENDENTES ---
const logoNeon = document.querySelector('.logo');
const logoOn = document.querySelector('.logo .accent');
const dropIcon = document.querySelector('.drop-icon');
const volumeIcon = document.querySelector('.volume-icon');
const allNeonBtns = document.querySelectorAll('.btn-neon');
const autoplayBtn = document.getElementById('btnToggleAutoplay');
const prevBtn = document.getElementById('btnPrev');
const nextBtn = document.getElementById('btnNext');
const fullscreenBtn = document.getElementById('btnFullscreen');

// --- PALETA DE CORES NEON (RGB) ---
const paletaNeon = [
    { r: 0, g: 255, b: 136, name: 'Verde' },
    { r: 255, g: 204, b: 0, name: 'Amarelo' },
    { r: 255, g: 51, b: 102, name: 'Vermelho' },
    { r: 0, g: 136, b: 255, name: 'Azul' },
    { r: 255, g: 102, b: 204, name: 'Rosa' },
    { r: 170, g: 68, b: 255, name: 'Roxo' },
    { r: 0, g: 255, b: 255, name: 'Ciano' },
    { r: 255, g: 128, b: 0, name: 'Laranja' }
];

// Cada elemento começa com um índice DIFERENTE para cores diferentes!
let colorIndex = {
    logoNeon: 0,
    logoOn: 1,
    dropIcon: 2,
    volumeIcon: 3,
    timeDisplay: 4,
    autoplayBtn: 5,
    navBtns: 6,
    neonBtns: 7,
    playBtn: 0,
    activeItem: 2
};

let colorInterval = null;

// --- FUNÇÕES DE COR ---
function rgbToString(r, g, b) {
    return `rgb(${r}, ${g}, ${b})`;
}

function getGlow(r, g, b) {
    return `0 0 10px rgba(${r}, ${g}, ${b}, 0.5)`;
}

// --- APLICA CORES INDEPENDENTES PARA CADA ELEMENTO ---
function applyAllColors() {
    // 1. Logo "Neon"
    const neonColor = paletaNeon[colorIndex.logoNeon % paletaNeon.length];
    if (logoNeon) {
        logoNeon.style.color = rgbToString(neonColor.r, neonColor.g, neonColor.b);
        logoNeon.style.textShadow = getGlow(neonColor.r, neonColor.g, neonColor.b);
    }
    
    // 2. Logo "On"
    const onColor = paletaNeon[colorIndex.logoOn % paletaNeon.length];
    if (logoOn) {
        logoOn.style.color = rgbToString(onColor.r, onColor.g, onColor.b);
        logoOn.style.textShadow = getGlow(onColor.r, onColor.g, onColor.b);
    }
    
    // 3. Ícone Drop
    const dropColor = paletaNeon[colorIndex.dropIcon % paletaNeon.length];
    if (dropIcon) {
        dropIcon.style.color = rgbToString(dropColor.r, dropColor.g, dropColor.b);
        dropIcon.style.textShadow = getGlow(dropColor.r, dropColor.g, dropColor.b);
    }
    
    // 4. Ícone Volume
    const volumeColor = paletaNeon[colorIndex.volumeIcon % paletaNeon.length];
    if (volumeIcon) {
        volumeIcon.style.color = rgbToString(volumeColor.r, volumeColor.g, volumeColor.b);
    }
    
    // 5. Display Tempo
    const timeColor = paletaNeon[colorIndex.timeDisplay % paletaNeon.length];
    if (timeDisplay) {
        timeDisplay.style.color = rgbToString(timeColor.r, timeColor.g, timeColor.b);
        timeDisplay.style.textShadow = getGlow(timeColor.r, timeColor.g, timeColor.b);
    }
    
    // 6. Botão Autoplay
    const autoplayColor = paletaNeon[colorIndex.autoplayBtn % paletaNeon.length];
    if (autoplayBtn) {
        autoplayBtn.style.color = rgbToString(autoplayColor.r, autoplayColor.g, autoplayColor.b);
        autoplayBtn.style.textShadow = getGlow(autoplayColor.r, autoplayColor.g, autoplayColor.b);
        autoplayBtn.style.borderColor = rgbToString(autoplayColor.r, autoplayColor.g, autoplayColor.b);
    }
    
    // 7. Botões Navegação
    const navColor = paletaNeon[colorIndex.navBtns % paletaNeon.length];
    if (prevBtn) {
        prevBtn.style.color = rgbToString(navColor.r, navColor.g, navColor.b);
        prevBtn.style.borderColor = rgbToString(navColor.r, navColor.g, navColor.b);
    }
    if (nextBtn) {
        nextBtn.style.color = rgbToString(navColor.r, navColor.g, navColor.b);
        nextBtn.style.borderColor = rgbToString(navColor.r, navColor.g, navColor.b);
    }
    if (fullscreenBtn) {
        fullscreenBtn.style.color = rgbToString(navColor.r, navColor.g, navColor.b);
        fullscreenBtn.style.borderColor = rgbToString(navColor.r, navColor.g, navColor.b);
    }
    
    // 8. Botões Neon
    const btnColor = paletaNeon[colorIndex.neonBtns % paletaNeon.length];
    allNeonBtns.forEach(btn => {
        btn.style.color = rgbToString(btnColor.r, btnColor.g, btnColor.b);
        btn.style.borderColor = rgbToString(btnColor.r, btnColor.g, btnColor.b);
    });
    
    // 9. Botão Play
    const playColor = paletaNeon[colorIndex.playBtn % paletaNeon.length];
    if (btnPlay) {
        btnPlay.style.color = rgbToString(playColor.r, playColor.g, playColor.b);
        btnPlay.style.borderColor = rgbToString(playColor.r, playColor.g, playColor.b);
        btnPlay.style.textShadow = getGlow(playColor.r, playColor.g, playColor.b);
    }
    
    // 10. Slider do Volume
    const sliderColor = paletaNeon[(colorIndex.volumeIcon + 2) % paletaNeon.length];
    let style = document.getElementById('dynamic-thumb-style');
    if (style) style.remove();
    style = document.createElement('style');
    style.id = 'dynamic-thumb-style';
    style.textContent = `input[type="range"]::-webkit-slider-thumb { 
        background: ${rgbToString(sliderColor.r, sliderColor.g, sliderColor.b)}; 
        box-shadow: 0 0 8px ${rgbToString(sliderColor.r, sliderColor.g, sliderColor.b)};
        transition: all 0.2s ease;
    }`;
    document.head.appendChild(style);
    
    // 11. Itens ativos
    const activeColor = paletaNeon[colorIndex.activeItem % paletaNeon.length];
    const activeListItems = document.querySelectorAll('.video-list li.active');
    activeListItems.forEach(item => {
        item.style.color = rgbToString(activeColor.r, activeColor.g, activeColor.b);
        item.style.borderLeftColor = rgbToString(activeColor.r, activeColor.g, activeColor.b);
        item.style.textShadow = getGlow(activeColor.r, activeColor.g, activeColor.b);
    });
}

// --- AVANÇA TODAS AS CORES ---
function advanceAllColors() {
    colorIndex.logoNeon++;
    colorIndex.logoOn++;
    colorIndex.dropIcon++;
    colorIndex.volumeIcon++;
    colorIndex.timeDisplay++;
    colorIndex.autoplayBtn++;
    colorIndex.navBtns++;
    colorIndex.neonBtns++;
    colorIndex.playBtn++;
    colorIndex.activeItem++;
    applyAllColors();
}

function startAutoColor() {
    if (colorInterval) clearInterval(colorInterval);
    colorInterval = setInterval(advanceAllColors, 2000);
}

// --- ESTADO ---
let mediaFiles = [];
let currentIndex = -1;
let autoplay = true;
let currentFolder = null;

const videoExtensions = ['.mp4', '.webm', '.ogg', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.m4v'];
const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.ico'];

// --- CONFIG ---
const CONFIG_KEY = 'neonon_config';

function loadConfig() {
    try {
        const saved = localStorage.getItem(CONFIG_KEY);
        if (saved) {
            const config = JSON.parse(saved);
            autoplay = config.autoplay ?? true;
            volumeSlider.value = config.volume ?? 100;
            videoPlayer.volume = volumeSlider.value / 100;
        }
    } catch (e) {
        console.warn('Erro ao carregar configurações:', e);
    }
}

function saveConfig() {
    const config = { autoplay: autoplay, volume: parseInt(volumeSlider.value) };
    localStorage.setItem(CONFIG_KEY, JSON.stringify(config));
}

// --- FUNÇÕES DE SEGURANÇA PARA REVOKE DE URLs ---
/**
 * Revoga uma URL de objeto com segurança
 * Apenas revoga URLs que começam com 'blob:'
 */
function safeRevoke(url) {
    if (url && typeof url === 'string' && url.startsWith('blob:')) {
        try {
            URL.revokeObjectURL(url);
            return true;
        } catch (e) {
            console.warn('Erro ao revogar URL:', e);
            return false;
        }
    }
    return false;
}

// --- SELEÇÃO DE PASTA ---
/**
 * Detecta se está rodando no PyWebView ou no navegador
 * e usa a API apropriada para selecionar pasta
 */
async function selectFolder() {
    // Verifica se está no PyWebView
    if (typeof pywebview !== 'undefined') {
        return await selectFolderPython();
    }
    // Modo navegador
    return await selectFolderBrowser();
}

/**
 * Modo Python - usa a API do PyWebView
 */
async function selectFolderPython() {
    try {
        const folderPath = await pywebview.api.open_folder_dialog();
        
        // Usuário cancelou
        if (!folderPath) {
            return false;
        }
        
        // Se retornou erro (ex: permissão negada)
        if (folderPath.error) {
            alert(`Erro: ${folderPath.error}`);
            return false;
        }
        
        // Obtém o conteúdo da pasta
        const result = await pywebview.api.get_folder_contents(folderPath);
        
        if (!result.success) {
            alert(`Erro ao listar arquivos: ${result.error || 'Erro desconhecido'}`);
            return false;
        }
        
        // Converte o resultado para o formato esperado
        mediaFiles = result.files.map(f => ({
            name: f.name,
            path: f.path,
            type: f.type,
            size: f.size
        }));
        
        currentIndex = -1;
        updateMediaList();
        
        if (mediaFiles.length > 0) {
            playMedia(0);
        } else {
            alert('Nenhum arquivo de vídeo ou imagem encontrado nesta pasta.');
        }
        
        return true;
        
    } catch (e) {
        console.error('Erro no selectFolderPython:', e);
        alert(`Erro ao acessar a pasta: ${e.message || 'Erro desconhecido'}`);
        return false;
    }
}

/**
 * Modo Navegador - usa File System Access API
 * Funciona apenas no Chrome/Edge com HTTPS
 */
async function selectFolderBrowser() {
    try {
        const dirHandle = await window.showDirectoryPicker();
        currentFolder = dirHandle;
        await loadMediaFromFolder(dirHandle);
        return true;
    } catch (err) {
        if (err.name !== 'AbortError') {
            console.error('Erro ao selecionar pasta:', err);
            alert('Erro ao acessar a pasta. Use Chrome ou Edge com HTTPS.');
        }
        return false;
    }
}

// --- CARREGAMENTO DE MÍDIA (MODO NAVEGADOR) ---
async function loadMediaFromFolder(dirHandle) {
    mediaFiles = [];
    for await (const entry of dirHandle.values()) {
        if (entry.kind === 'file') {
            const ext = '.' + entry.name.split('.').pop().toLowerCase();
            if (videoExtensions.includes(ext) || imageExtensions.includes(ext)) {
                mediaFiles.push(entry);
            }
        }
    }
    mediaFiles.sort((a, b) => a.name.localeCompare(b.name, 'pt-BR', { numeric: true }));
    updateMediaList();
    if (mediaFiles.length > 0) playMedia(0);
}

// --- ATUALIZA A LISTA DE ARQUIVOS ---
function updateMediaList() {
    videoList.innerHTML = '';
    if (mediaFiles.length === 0) {
        videoList.innerHTML = '<li class="empty-state">Nenhum arquivo encontrado</li>';
        videoCounter.textContent = '';
        return;
    }
    mediaFiles.forEach((file, index) => {
        const li = document.createElement('li');
        const ext = '.' + file.name.split('.').pop().toLowerCase();
        const isImage = imageExtensions.includes(ext);
        const icon = isImage ? '🖼️ ' : '🎬 ';
        li.innerHTML = icon + file.name;
        li.addEventListener('click', () => playMedia(index));
        if (index === currentIndex) li.classList.add('active');
        videoList.appendChild(li);
    });
    videoCounter.textContent = `${mediaFiles.length} arquivo${mediaFiles.length !== 1 ? 's' : ''}`;
}

// --- REPRODUZ MÍDIA ---
async function playMedia(index) {
    if (index < 0 || index >= mediaFiles.length) return;
    currentIndex = index;
    const file = mediaFiles[index];
    
    try {
        let url;
        let isImage = false;
        const ext = '.' + file.name.split('.').pop().toLowerCase();
        isImage = imageExtensions.includes(ext);
        
        // Detecta o tipo de objeto e gera URL apropriada
        if (typeof file.getFile === 'function') {
            // Modo navegador - FileSystemFileHandle
            const fileData = await file.getFile();
            url = URL.createObjectURL(fileData);
        } else if (file.path) {
            // Modo Python - objeto com caminho
            // Converte para formato URL file://
            const normalizedPath = file.path.replace(/\\/g, '/');
            url = `file:///${normalizedPath}`;
        } else {
            throw new Error('Formato de arquivo não suportado');
        }
        
        // Revoga URLs antigas de forma segura
        safeRevoke(videoPlayer.src);
        safeRevoke(imageViewer.src);
        
        if (isImage) {
            imageViewer.src = url;
            imageViewer.style.display = 'block';
            videoPlayer.style.display = 'none';
            videoPlayer.pause();
            timeDisplay.textContent = `🖼️ ${file.name}`;
            btnPlay.innerHTML = '🖼️';
        } else {
            videoPlayer.src = url;
            videoPlayer.style.display = 'block';
            imageViewer.style.display = 'none';
            videoPlayer.load();
            videoPlayer.play();
            updatePlayButton();
        }
        
        videoContainer.classList.add('has-video');
        dropOverlay.style.display = 'none';
        updateMediaList();
        highlightCurrentInList();
        applyAllColors();
        
    } catch (err) {
        console.error('Erro ao carregar arquivo:', err);
        alert(`Erro ao carregar o arquivo: ${err.message || 'Erro desconhecido'}`);
    }
}

function highlightCurrentInList() {
    const items = videoList.querySelectorAll('li');
    items.forEach((item, i) => {
        if (i === currentIndex) {
            item.classList.add('active');
            item.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } else {
            item.classList.remove('active');
        }
    });
}

// --- CONTROLES ---
btnPlay.addEventListener('click', togglePlay);
videoPlayer.addEventListener('click', togglePlay);

function togglePlay() {
    if (imageViewer.style.display === 'block') return;
    if (videoPlayer.paused) videoPlayer.play();
    else videoPlayer.pause();
    updatePlayButton();
}

function updatePlayButton() {
    if (imageViewer.style.display === 'block') {
        btnPlay.innerHTML = '🖼️';
        return;
    }
    btnPlay.innerHTML = videoPlayer.paused ? '▶' : '❚❚';
}

btnPrev.addEventListener('click', () => {
    if (mediaFiles.length === 0) return;
    playMedia(currentIndex > 0 ? currentIndex - 1 : mediaFiles.length - 1);
});

btnNext.addEventListener('click', () => {
    if (mediaFiles.length === 0) return;
    playMedia(currentIndex < mediaFiles.length - 1 ? currentIndex + 1 : 0);
});

// --- AUTOPLAY MELHORADO ---
btnToggleAutoplay.addEventListener('click', () => {
    autoplay = !autoplay;
    updateAutoplayButton();
    saveConfig();
});

function updateAutoplayButton() {
    if (autoplay) {
        autoplayBtn.innerHTML = '▶';
        autoplayBtn.title = 'Autoplay: Ligado';
        autoplayBtn.classList.remove('autoplay-off');
        autoplayBtn.classList.add('autoplay-on');
        // Restaura a cor neon
        autoplayBtn.style.color = '';
        autoplayBtn.style.textShadow = '';
        autoplayBtn.style.borderColor = '';
    } else {
        autoplayBtn.innerHTML = '⏸';
        autoplayBtn.title = 'Autoplay: Desligado';
        autoplayBtn.classList.add('autoplay-off');
        autoplayBtn.classList.remove('autoplay-on');
        // Indica visualmente que está desligado
        autoplayBtn.style.color = '#8888aa';
        autoplayBtn.style.textShadow = 'none';
        autoplayBtn.style.borderColor = 'transparent';
    }
}

videoPlayer.addEventListener('ended', () => {
    if (autoplay && mediaFiles.length > 1) {
        btnNext.click();
    } else {
        updatePlayButton();
    }
});

// --- VOLUME ---
volumeSlider.addEventListener('input', () => {
    videoPlayer.volume = volumeSlider.value / 100;
    saveConfig();
});

// --- BARRA DE PROGRESSO ---
videoPlayer.addEventListener('timeupdate', () => {
    if (videoPlayer.duration && !isNaN(videoPlayer.duration)) {
        const percent = (videoPlayer.currentTime / videoPlayer.duration) * 100;
        progressBar.value = percent;
    }
    if (imageViewer.style.display === 'block') return;
    timeDisplay.textContent = `${formatTime(videoPlayer.currentTime)} / ${formatTime(videoPlayer.duration)}`;
});

progressBar.addEventListener('input', () => {
    if (videoPlayer.duration) {
        videoPlayer.currentTime = (progressBar.value / 100) * videoPlayer.duration;
    }
});

function formatTime(seconds) {
    if (isNaN(seconds) || !isFinite(seconds)) return '00:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

// --- TELA CHEIA ---
btnFullscreen.addEventListener('click', () => {
    if (document.fullscreenElement) {
        document.exitFullscreen();
    } else {
        videoContainer.requestFullscreen();
    }
});

// --- BOTÃO RESET ---
btnReset.addEventListener('click', resetPlayer);

function resetPlayer() {
    if (mediaFiles.length === 0) return;
    if (confirm('Deseja limpar a lista e recomeçar?')) {
        // Revoga URLs de forma segura
        safeRevoke(videoPlayer.src);
        safeRevoke(imageViewer.src);
        
        mediaFiles = [];
        currentIndex = -1;
        videoPlayer.pause();
        videoPlayer.src = '';
        videoPlayer.style.display = 'none';
        imageViewer.src = '';
        imageViewer.style.display = 'none';
        timeDisplay.textContent = '00:00 / 00:00';
        btnPlay.innerHTML = '▶';
        dropOverlay.style.display = 'flex';
        videoContainer.classList.remove('has-video');
        updateMediaList();
        currentFolder = null;
        localStorage.removeItem('neonon_last_folder');
        const style = document.getElementById('dynamic-thumb-style');
        if (style) style.remove();
        progressBar.value = 0;
    }
}

// --- DRAG & DROP ---
document.addEventListener('dragover', (e) => {
    e.preventDefault();
    document.body.classList.add('dragover');
});

document.addEventListener('dragleave', (e) => {
    e.preventDefault();
    if (e.relatedTarget === null) {
        document.body.classList.remove('dragover');
    }
});

document.addEventListener('drop', async (e) => {
    e.preventDefault();
    document.body.classList.remove('dragover');
    
    const items = e.dataTransfer.items;
    if (!items) return;
    
    for (const item of items) {
        if (item.kind === 'file') {
            try {
                const entry = await item.getAsFileSystemHandle();
                if (entry && entry.kind === 'directory') {
                    currentFolder = entry;
                    await loadMediaFromFolder(entry);
                    return;
                }
            } catch (err) {
                console.warn('Erro ao processar drag & drop:', err);
            }
        }
    }
    
    const files = [...e.dataTransfer.files].filter(f => 
        f.type.startsWith('video/') || f.type.startsWith('image/')
    );
    if (files.length > 0) {
        alert('Arraste uma pasta inteira com vídeos e imagens.');
    }
});

// --- ATALHOS DE TECLADO ---
document.addEventListener('keydown', (e) => {
    // Ignora se estiver em um campo de input
    if (e.target.tagName === 'INPUT') return;
    
    switch(e.key) {
        case ' ':
            if (imageViewer.style.display !== 'block') {
                e.preventDefault();
                togglePlay();
            }
            break;
        case 'ArrowLeft':
            e.preventDefault();
            btnPrev.click();
            break;
        case 'ArrowRight':
            e.preventDefault();
            btnNext.click();
            break;
        case 'f':
        case 'F':
            e.preventDefault();
            btnFullscreen.click();
            break;
        case 'ArrowUp':
            e.preventDefault();
            volumeSlider.value = Math.min(100, parseInt(volumeSlider.value) + 5);
            videoPlayer.volume = volumeSlider.value / 100;
            saveConfig();
            break;
        case 'ArrowDown':
            e.preventDefault();
            volumeSlider.value = Math.max(0, parseInt(volumeSlider.value) - 5);
            videoPlayer.volume = volumeSlider.value / 100;
            saveConfig();
            break;
        case 'm':
        case 'M':
            e.preventDefault();
            // Mute/Unmute
            if (videoPlayer.volume > 0) {
                videoPlayer._lastVolume = videoPlayer.volume;
                videoPlayer.volume = 0;
                volumeSlider.value = 0;
            } else {
                videoPlayer.volume = videoPlayer._lastVolume || 1;
                volumeSlider.value = videoPlayer.volume * 100;
            }
            saveConfig();
            break;
    }
});

// ============================================
// INTEGRAÇÃO COM PYTHON (PyWebView)
// ============================================

const isPython = typeof pywebview !== 'undefined';

if (isPython) {
    console.log('🐍 Modo Python ativado!');
    
    // Substitui o evento do botão
    btnSelectFolder.onclick = async function() {
        await selectFolder();
    };
    
    // Carregar preferências do Python
    async function loadPythonPreferences() {
        try {
            const prefs = await pywebview.api.load_preferences();
            if (prefs && !prefs.error) {
                if (prefs.autoplay !== undefined) {
                    autoplay = prefs.autoplay;
                    updateAutoplayButton();
                }
                if (prefs.volume !== undefined) {
                    volumeSlider.value = prefs.volume;
                    videoPlayer.volume = prefs.volume / 100;
                }
            }
        } catch (e) {
            console.warn('Erro ao carregar preferências do Python:', e);
        }
    }
    
    loadPythonPreferences();
    
    // Salvar preferências no Python
    function savePythonPreferences() {
        try {
            pywebview.api.save_preferences({
                volume: parseInt(volumeSlider.value),
                autoplay: autoplay
            });
        } catch (e) {
            console.warn('Erro ao salvar preferências no Python:', e);
        }
    }
    
    // Adiciona eventos para salvar automaticamente
    volumeSlider.addEventListener('input', () => {
        videoPlayer.volume = volumeSlider.value / 100;
        savePythonPreferences();
        saveConfig();
    });
    
    btnToggleAutoplay.addEventListener('click', () => {
        setTimeout(() => {
            savePythonPreferences();
            saveConfig();
        }, 100);
    });
    
    console.log('✅ Integração Python completa!');
} else {
    console.log('🌐 Modo Navegador ativado');
    btnSelectFolder.onclick = selectFolder;
}

// --- INICIALIZAÇÃO ---
loadConfig();
updateAutoplayButton();
updatePlayButton();
applyAllColors();
startAutoColor();

console.log('%c✨ NeonOn - Desenvolvido por Misa ✨', 'color: #ff66cc; font-size: 14px;');
console.log('%c🌈 CADA ELEMENTO tem sua PRÓPRIA COR neon!', 'color: #ffcc00; font-size: 12px;');
console.log('%c🎯 Player de mídia profissional com cores dinâmicas!', 'color: #00ff88; font-size: 12px;');