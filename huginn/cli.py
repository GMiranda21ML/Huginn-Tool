import argparse
import sys

from huginn import __version__
from huginn.core import banner, logger
from huginn.core.authorization import confirm_authorization
from huginn.core.output import prepare_output_dir
from huginn.integrations import github
from huginn.passive import dnsdumpster, wayback, whois_lookup
from huginn.passive import manual_links as passive_links
from huginn.active import banner_grab, dotgit, headers as http_headers, source_analysis, subdomains, waf_detect, whatweb
from huginn.active import manual_links as active_links


PASSIVE_MODULES = [
    ("Whois", whois_lookup),
    ("Wayback Machine", wayback),
    ("DNSDumpster (precisa de HUGINN_DNSDUMPSTER_API_KEY no .env, opcional)", dnsdumpster),
    ("GitHub (funciona sem chave; HUGINN_GITHUB_TOKEN no .env habilita busca de código)", github),
    ("Dorks/links manuais (Google, LinkedIn, MetaCrawler, OSINT Framework, Netcraft)", passive_links),
]

ACTIVE_MODULES = [
    ("Enumeração de subdomínios (subfinder)", subdomains),
    ("WhatWeb (fingerprint de tecnologia)", whatweb),
    ("Link manual (BuiltWith/Wappalyzer)", active_links),
    ("DotGit exposed", dotgit),
    ("Detecção de WAF (wafw00f)", waf_detect),
    ("Cabeçalhos HTTP + headers de segurança ausentes", http_headers),
    ("Banner grabbing (nmap -sV, top 1000 portas)", banner_grab),
    ("Análise de código-fonte", source_analysis),
]


def _module_list_text(modules):
    return "\n".join(f"    - {label}" for label, _ in modules)


def build_parser():
    epilog = f"""\
Módulos executados em --passive:
{_module_list_text(PASSIVE_MODULES)}

Módulos executados em --active (exige confirmação de autorização):
{_module_list_text(ACTIVE_MODULES)}

Exemplos:
  huginn -d dominio.com.br --passive
  huginn -d dominio.com.br --active
  huginn -d dominio.com.br --all

Saída salva em: output/<domínio>/passive/ e output/<domínio>/active/
Chaves de API opcionais (DNSDumpster, GitHub) vão no arquivo .env na raiz do projeto (veja .env.example).
"""
    parser = argparse.ArgumentParser(
        prog="huginn",
        description="Huginn — ferramenta de reconhecimento passivo e ativo para pentest.",
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-d", "--domain", required=True, help="Domínio alvo (ex: dominio.com.br)")
    parser.add_argument("--passive", action="store_true", help="Executa o reconhecimento passivo (sem tocar a infraestrutura do alvo)")
    parser.add_argument("--active", action="store_true", help="Executa o reconhecimento ativo (interage direto com o alvo; exige confirmação)")
    parser.add_argument("--all", action="store_true", help="Executa passivo e ativo")
    parser.add_argument("--version", action="version", version=f"huginn {__version__}")
    return parser


def run_passive(domain, output_dir):
    passive_dir = output_dir / "passive"
    passive_dir.mkdir(parents=True, exist_ok=True)

    results = {}
    for label, module in PASSIVE_MODULES:
        results[label] = module.run(domain, passive_dir)
    return results


def run_active(domain, output_dir):
    active_dir = output_dir / "active"
    active_dir.mkdir(parents=True, exist_ok=True)

    results = {}
    for label, module in ACTIVE_MODULES:
        results[label] = module.run(domain, active_dir)
    return results


def main(argv=None):
    banner.show()
    parser = build_parser()
    args = parser.parse_args(argv)

    if not (args.passive or args.active or args.all):
        parser.error("informe pelo menos um modo: --passive, --active ou --all")

    do_passive = args.passive or args.all
    do_active = args.active or args.all

    output_dir = prepare_output_dir(args.domain)
    logger.ok(f"Alvo: {args.domain}")
    logger.ok(f"Diretório de saída: {output_dir}")

    if do_active and not confirm_authorization(args.domain):
        logger.err("Autorização não confirmada. Abortando reconhecimento ativo.")
        sys.exit(1)

    if do_passive:
        run_passive(args.domain, output_dir)

    if do_active:
        run_active(args.domain, output_dir)
