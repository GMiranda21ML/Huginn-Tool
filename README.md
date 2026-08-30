# 🐦‍⬛ Huginn

**Huginn** é uma ferramenta de linha de comando para reconhecimento passivo e ativo em pentests, escrita em Python. Ela automatiza a coleta de informações sobre um domínio-alvo e gera um relatório em PDF ao final.

> ⚠️ **Uso ético e legal**: o módulo de reconhecimento ativo interage diretamente com a infraestrutura do alvo (scans de porta, requisições HTTP, etc). Use o Huginn **apenas** contra domínios para os quais você possui autorização explícita e por escrito. A ferramenta exige confirmação manual antes de rodar qualquer módulo ativo.

## Funcionalidades

### Reconhecimento passivo (`--passive`)
Não toca a infraestrutura do alvo — coleta informações de fontes públicas/terceiros.

| Módulo | Descrição |
|---|---|
| `whois` | Consulta WHOIS do domínio |
| `wayback` | Histórico de URLs via Wayback Machine |
| `dnsdumpster` | Enumeração via DNSDumpster (opcional, requer API key) |
| `github` | Busca por menções/código relacionado ao alvo no GitHub |
| `dorks` | Links prontos para dorks manuais (Google, LinkedIn, MetaCrawler, OSINT Framework, Netcraft) |

### Reconhecimento ativo (`--active`)
Interage diretamente com o alvo — **exige confirmação de autorização**.

| Módulo | Descrição |
|---|---|
| `subdomains` | Enumeração de subdomínios (via `subfinder`) |
| `whatweb` | Fingerprint de tecnologias (via `whatweb`) |
| `wappalyzer` | Link manual para BuiltWith/Wappalyzer |
| `dotgit` | Verificação de exposição de `.git` |
| `wafw00f` | Detecção de WAF (via `wafw00f`) |
| `headers` | Análise de cabeçalhos HTTP e headers de segurança ausentes |
| `nmap` | Banner grabbing com `nmap -sV` (top 1000 portas) |
| `source` | Análise do código-fonte da página |

### Relatório
Com `--report`, o Huginn compila todos os dados já coletados em `output/<domínio>/` e gera um PDF (`output/<domínio>/relatorio.pdf`) com os achados (usando `weasyprint` e classificação de severidade via `cvss`).

## Instalação

Suporte para **Debian/Ubuntu/Kali** e **Arch/Manjaro**.

```bash
git clone https://github.com/<seu-usuario>/Huginn-Tool.git
cd Huginn-Tool
chmod +x install.sh
./install.sh
```

O script `install.sh`:
- detecta a distro e instala dependências de sistema (`nmap`, `whois`, `ruby`, libs do WeasyPrint, etc);
- cria um ambiente virtual Python em `.venv/`;
- instala ferramentas de reconhecimento (`whatweb`, `wafw00f`, `subfinder`), com fallback via pip/git quando não há pacote nativo;
- instala as dependências Python do motor de relatório (`requirements.txt`);
- cria o link simbólico global `huginn` em `/usr/local/bin`.

Ao final, você pode rodar `huginn` de qualquer diretório.

### Configuração (opcional)

Algumas integrações usam chaves de API opcionais. Copie o exemplo e preencha:

```bash
cp .env.example .env
```

```env
HUGINN_DNSDUMPSTER_API_KEY=
HUGINN_GITHUB_TOKEN=
```

- `HUGINN_DNSDUMPSTER_API_KEY`: habilita o módulo `dnsdumpster`.
- `HUGINN_GITHUB_TOKEN`: habilita busca de código no módulo `github` (sem o token, o módulo ainda funciona, mas com limitações).

## Uso

```bash
huginn -d dominio.com.br --passive              # só reconhecimento passivo
huginn -d dominio.com.br --active               # só reconhecimento ativo (pede confirmação)
huginn -d dominio.com.br --all                  # passivo + ativo
huginn -d dominio.com.br --only whois github     # roda só módulos específicos
huginn -d dominio.com.br --all --report          # coleta tudo e já gera o PDF
huginn -d dominio.com.br --report                # gera o PDF a partir do que já foi coletado
```

### Opções

| Flag | Descrição |
|---|---|
| `-d`, `--domain` | Domínio alvo (obrigatório) |
| `--passive` | Executa o reconhecimento passivo |
| `--active` | Executa o reconhecimento ativo (exige confirmação de autorização) |
| `--all` | Executa passivo e ativo |
| `--only MODULO [MODULO ...]` | Roda apenas os módulos informados (aceita vários) |
| `--report` | Gera o relatório em PDF a partir dos dados já coletados |
| `--version` | Mostra a versão instalada |

### Saída

```
output/<domínio>/
├── passive/          # resultados dos módulos passivos
├── active/           # resultados dos módulos ativos
└── relatorio.pdf     # relatório final (gerado com --report)
```

## Estrutura do projeto

```
huginn/
├── cli.py                  # parsing de argumentos e orquestração
├── core/                   # config, logger, banner, autorização, saída
├── passive/                # módulos de reconhecimento passivo
├── active/                 # módulos de reconhecimento ativo
├── integrations/           # integrações externas (ex: GitHub)
└── report/                 # coleta de achados, renderização e PDF
bin/huginn                  # wrapper executável
install.sh                  # instalador de dependências
```

## Requisitos

- Python 3
- Distro baseada em Debian/Ubuntu/Kali ou Arch/Manjaro
- Ferramentas externas: `nmap`, `whois`, `whatweb`, `wafw00f`, `subfinder` (instaladas automaticamente pelo `install.sh`)
- Dependências Python: `weasyprint`, `cvss` (ver `requirements.txt`)

## Aviso legal

Esta ferramenta é destinada exclusivamente a testes de segurança autorizados. O uso contra sistemas sem consentimento explícito do proprietário é ilegal. Os autores não se responsabilizam por uso indevido.
