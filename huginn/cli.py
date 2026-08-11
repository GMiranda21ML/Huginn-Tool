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
from huginn.report import generate_report


PASSIVE_MODULES = [
    ("whois", "Whois", whois_lookup),
    ("wayback", "Wayback Machine", wayback),
    ("dnsdumpster", "DNSDumpster (precisa de HUGINN_DNSDUMPSTER_API_KEY no .env, opcional)", dnsdumpster),
    ("github", "GitHub (funciona sem chave; HUGINN_GITHUB_TOKEN no .env habilita busca de código)", github),
    ("dorks", "Dorks/links manuais (Google, LinkedIn, MetaCrawler, OSINT Framework, Netcraft)", passive_links),
]

ACTIVE_MODULES = [
    ("subdomains", "Enumeração de subdomínios (subfinder)", subdomains),
    ("whatweb", "WhatWeb (fingerprint de tecnologia)", whatweb),
    ("wappalyzer", "Link manual (BuiltWith/Wappalyzer)", active_links),
    ("dotgit", "DotGit exposed", dotgit),
    ("wafw00f", "Detecção de WAF (wafw00f)", waf_detect),
    ("headers", "Cabeçalhos HTTP + headers de segurança ausentes", http_headers),
    ("nmap", "Banner grabbing (nmap -sV, top 1000 portas)", banner_grab),
    ("source", "Análise de código-fonte", source_analysis),
]

ALL_MODULES = {
    **{slug: ("passive", label, module) for slug, label, module in PASSIVE_MODULES},
    **{slug: ("active", label, module) for slug, label, module in ACTIVE_MODULES},
}


def _module_list_text(modules):
    return "\n".join(f"    {slug:<12} {label}" for slug, label, _ in modules)


def build_parser():
    epilog = f"""\
Módulos passivos (--passive ou --only <slug>; sem tocar a infraestrutura do alvo):
{_module_list_text(PASSIVE_MODULES)}

Módulos ativos (--active ou --only <slug>; exige confirmação de autorização):
{_module_list_text(ACTIVE_MODULES)}

Exemplos:
  huginn -d dominio.com.br --passive
  huginn -d dominio.com.br --active
  huginn -d dominio.com.br --all
  huginn -d dominio.com.br --only whois github
  huginn -d dominio.com.br --all --report
  huginn -d dominio.com.br --report                 (gera o PDF a partir do que já foi coletado)

Saída salva em: output/<domínio>/passive/ e output/<domínio>/active/
Relatório em PDF salvo em: output/<domínio>/relatorio.pdf
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
    parser.add_argument(
        "--only",
        nargs="+",
        metavar="MODULO",
        help="Roda só os módulos informados (aceita vários, separados por espaço ou vírgula). Veja a lista de slugs abaixo.",
    )
    parser.add_argument("--report", action="store_true", help="Gera o relatório em PDF a partir dos dados coletados em output/<domínio>/")
    parser.add_argument("--version", action="version", version=f"huginn {__version__}")
    return parser


def run_passive(domain, output_dir, modules=None):
    passive_dir = output_dir / "passive"
    passive_dir.mkdir(parents=True, exist_ok=True)

    results = {}
    for slug, _, module in modules if modules is not None else PASSIVE_MODULES:
        results[slug] = module.run(domain, passive_dir)
    return results


def run_active(domain, output_dir, modules=None):
    active_dir = output_dir / "active"
    active_dir.mkdir(parents=True, exist_ok=True)

    results = {}
    for slug, _, module in modules if modules is not None else ACTIVE_MODULES:
        results[slug] = module.run(domain, active_dir)
    return results


def _resolve_only(parser, only_args):
    slugs = []
    for item in only_args:
        slugs.extend(s.strip() for s in item.split(",") if s.strip())

    invalid = [s for s in slugs if s not in ALL_MODULES]
    if invalid:
        parser.error(f"módulo(s) inválido(s) em --only: {', '.join(invalid)}. Use --help para ver os slugs disponíveis.")

    passive_selected = [(slug, ALL_MODULES[slug][1], ALL_MODULES[slug][2]) for slug in slugs if ALL_MODULES[slug][0] == "passive"]
    active_selected = [(slug, ALL_MODULES[slug][1], ALL_MODULES[slug][2]) for slug in slugs if ALL_MODULES[slug][0] == "active"]
    return passive_selected, active_selected


def main(argv=None):
    banner.show()
    parser = build_parser()
    args = parser.parse_args(argv)

    if not (args.passive or args.active or args.all or args.only or args.report):
        parser.error("informe pelo menos um modo: --passive, --active, --all, --only ou --report")

    output_dir = prepare_output_dir(args.domain)
    logger.ok(f"Alvo: {args.domain}")
    logger.ok(f"Diretório de saída: {output_dir}")

    if args.only:
        passive_selected, active_selected = _resolve_only(parser, args.only)

        if active_selected and not confirm_authorization(args.domain):
            logger.err("Autorização não confirmada. Abortando.")
            sys.exit(1)

        if passive_selected:
            run_passive(args.domain, output_dir, modules=passive_selected)
        if active_selected:
            run_active(args.domain, output_dir, modules=active_selected)
    else:
        do_passive = args.passive or args.all
        do_active = args.active or args.all

        if do_active and not confirm_authorization(args.domain):
            logger.err("Autorização não confirmada. Abortando reconhecimento ativo.")
            sys.exit(1)

        if do_passive:
            run_passive(args.domain, output_dir)
        if do_active:
            run_active(args.domain, output_dir)

    if args.report:
        passive_dir = output_dir / "passive"
        active_dir = output_dir / "active"
        if not any(passive_dir.glob("*")) and not any(active_dir.glob("*")):
            logger.warn("Nenhum dado coletado para esse domínio ainda — rode --passive/--active/--all antes de --report.")
        else:
            logger.info("Gerando relatório em PDF a partir dos dados coletados...")
            report_path = generate_report(args.domain, output_dir)
            logger.ok(f"Relatório salvo em {report_path}")
