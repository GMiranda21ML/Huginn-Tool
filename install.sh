#!/usr/bin/env bash
#
# Instalador do Huginn — detecta a distro (Debian/Ubuntu/Kali ou Arch) e
# instala as ferramentas de reconhecimento usadas pelos módulos passivo e
# ativo, além de preparar o venv Python para o motor de relatório.
set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_ROOT/.venv"
TOOLS_DIR="$PROJECT_ROOT/.tools"
BIN_TARGET="/usr/local/bin"

declare -A TOOL_STATUS

if [ "$(id -u)" -ne 0 ]; then
    SUDO="sudo"
else
    SUDO=""
fi

# ---------------------------------------------------------------------------
# logging
# ---------------------------------------------------------------------------
c_info() { printf '\033[34m[*]\033[0m %s\n' "$1"; }
c_ok()   { printf '\033[32m[+]\033[0m %s\n' "$1"; }
c_warn() { printf '\033[33m[!]\033[0m %s\n' "$1"; }
c_err()  { printf '\033[31m[-]\033[0m %s\n' "$1"; }

mark() { TOOL_STATUS["$1"]="$2"; } # mark <tool> <ok|fail|skip>

# ---------------------------------------------------------------------------
# detecção de distro
# ---------------------------------------------------------------------------
FAMILY=""
if [ -f /etc/os-release ]; then
    # shellcheck disable=SC1091
    . /etc/os-release
    case " ${ID:-} ${ID_LIKE:-} " in
        *debian*|*ubuntu*|*kali*) FAMILY="debian" ;;
        *arch*)                    FAMILY="arch" ;;
    esac
fi

if [ -z "$FAMILY" ]; then
    c_err "Distro não suportada (esperado: Debian/Ubuntu/Kali ou Arch/Manjaro)."
    exit 1
fi
c_ok "Distro detectada: ${PRETTY_NAME:-desconhecida} (família: $FAMILY)"

# ---------------------------------------------------------------------------
# helpers de instalação por gerenciador de pacotes
# ---------------------------------------------------------------------------
apt_install() {
    $SUDO apt-get install -y "$1" >/dev/null 2>&1
}

pacman_install() {
    $SUDO pacman -S --noconfirm --needed "$1" >/dev/null 2>&1
}

pip_install() {
    "$VENV_DIR/bin/pip" install -q "$1" >/dev/null 2>&1
}

try_install_native() {
    # try_install_native <apt_pkg> <pacman_pkg>
    if [ "$FAMILY" = "debian" ]; then
        apt_install "$1"
    else
        pacman_install "$2"
    fi
}

# ---------------------------------------------------------------------------
# atualização de índices
# ---------------------------------------------------------------------------
c_info "Atualizando índice de pacotes..."
if [ "$FAMILY" = "debian" ]; then
    $SUDO apt-get update -y >/dev/null 2>&1
else
    $SUDO pacman -Sy --noconfirm >/dev/null 2>&1
fi

# ---------------------------------------------------------------------------
# pacotes base (sempre via gerenciador nativo)
# ---------------------------------------------------------------------------
c_info "Instalando dependências base do sistema..."
BASE_DEBIAN=(curl whois nmap git unzip python3 python3-venv python3-pip ruby ruby-dev build-essential libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info fonts-liberation)
BASE_ARCH=(curl whois nmap git unzip python python-pip ruby base-devel pango cairo gdk-pixbuf2 libffi noto-fonts)

if [ "$FAMILY" = "debian" ]; then
    for pkg in "${BASE_DEBIAN[@]}"; do
        if apt_install "$pkg"; then mark "$pkg" ok; else mark "$pkg" fail; fi
    done
else
    for pkg in "${BASE_ARCH[@]}"; do
        if pacman_install "$pkg"; then mark "$pkg" ok; else mark "$pkg" fail; fi
    done
fi

# ---------------------------------------------------------------------------
# venv python (necessário: Debian 12+/Ubuntu 23.10+/Arch marcam o Python de
# sistema como "externally managed", pip direto no sistema não funciona)
# ---------------------------------------------------------------------------
c_info "Criando ambiente virtual Python em $VENV_DIR..."
if python3 -m venv "$VENV_DIR" 2>/dev/null; then
    "$VENV_DIR/bin/pip" install -q --upgrade pip >/dev/null 2>&1
    mark "venv" ok
else
    c_err "Falha ao criar o venv Python. Abortando."
    exit 1
fi

# ---------------------------------------------------------------------------
# ferramentas de reconhecimento: tenta pacote nativo, cai para pip, cai para
# git+build manual, e por último avisa que ficou indisponível.
# ---------------------------------------------------------------------------
mkdir -p "$TOOLS_DIR"

install_whatweb() {
    if try_install_native whatweb whatweb; then mark whatweb ok; return; fi
    c_warn "whatweb não disponível no repositório nativo, instalando via git+bundler..."
    if [ ! -d "$TOOLS_DIR/WhatWeb" ]; then
        git clone --depth 1 https://github.com/urbanadventurer/WhatWeb.git "$TOOLS_DIR/WhatWeb" >/dev/null 2>&1
    fi
    if [ -f "$TOOLS_DIR/WhatWeb/whatweb" ]; then
        gem install --user-install bundler --no-document >/dev/null 2>&1
        (cd "$TOOLS_DIR/WhatWeb" && bundle install >/dev/null 2>&1)
        chmod +x "$TOOLS_DIR/WhatWeb/whatweb"
        $SUDO ln -sf "$TOOLS_DIR/WhatWeb/whatweb" "$BIN_TARGET/whatweb"
        mark whatweb ok
    else
        mark whatweb fail
    fi
}

install_wafw00f() {
    if try_install_native wafw00f wafw00f; then mark wafw00f ok; return; fi
    if pip_install wafw00f; then
        $SUDO ln -sf "$VENV_DIR/bin/wafw00f" "$BIN_TARGET/wafw00f"
        mark wafw00f ok
    else
        mark wafw00f fail
    fi
}

install_subfinder() {
    if command -v subfinder >/dev/null 2>&1; then mark subfinder ok; return; fi
    c_info "Baixando subfinder (binário oficial via GitHub releases)..."
    local url
    url=$(curl -fsSL https://api.github.com/repos/projectdiscovery/subfinder/releases/latest \
        | grep browser_download_url | grep linux_amd64 | cut -d '"' -f4 | head -n1)
    if [ -z "$url" ]; then
        mark subfinder fail
        return
    fi
    local tmp
    tmp=$(mktemp -d)
    if curl -fsSL "$url" -o "$tmp/subfinder.zip" >/dev/null 2>&1 \
        && unzip -oq "$tmp/subfinder.zip" -d "$tmp" >/dev/null 2>&1 \
        && $SUDO install -m 755 "$tmp/subfinder" "$BIN_TARGET/subfinder"; then
        mark subfinder ok
    else
        mark subfinder fail
    fi
    rm -rf "$tmp"
}

c_info "Instalando ferramentas de reconhecimento..."
install_whatweb
install_wafw00f
install_subfinder

# ---------------------------------------------------------------------------
# dependências python do motor de relatório (dentro do venv)
# ---------------------------------------------------------------------------
c_info "Instalando dependências Python (relatório/CVSS) no venv..."
if "$VENV_DIR/bin/pip" install -q -r "$PROJECT_ROOT/requirements.txt" >/dev/null 2>&1; then
    mark "relatorio(weasyprint+cvss)" ok
else
    mark "relatorio(weasyprint+cvss)" fail
fi

# ---------------------------------------------------------------------------
# link global do executável huginn
# ---------------------------------------------------------------------------
chmod +x "$PROJECT_ROOT/bin/huginn"
if $SUDO ln -sf "$PROJECT_ROOT/bin/huginn" "$BIN_TARGET/huginn"; then
    mark "huginn (comando global)" ok
else
    mark "huginn (comando global)" fail
fi

# ---------------------------------------------------------------------------
# resumo final
# ---------------------------------------------------------------------------
echo
c_info "Resumo da instalação:"
FAILED=0
for tool in "${!TOOL_STATUS[@]}"; do
    status="${TOOL_STATUS[$tool]}"
    case "$status" in
        ok)   c_ok "$tool" ;;
        skip) c_warn "$tool (não instalado, com fallback disponível)" ;;
        fail) c_err "$tool"; FAILED=1 ;;
    esac
done

echo
if [ "$FAILED" -eq 1 ]; then
    c_warn "Alguns itens falharam — revise as mensagens acima antes de rodar o huginn."
else
    c_ok "Tudo pronto. Rode: huginn -d dominio.com.br --all"
fi
