import argparse
import sys

from huginn import __version__
from huginn.core import logger
from huginn.core.authorization import confirm_authorization
from huginn.core.output import prepare_output_dir

PASSIVE_ROADMAP = [
    "MetaCrawler",
    "Google Hacking (dorks)",
    "LinkedIn",
    "Whois",
    "Wayback Machine",
    "Netcraft / DNSDumpster",
    "OSINT Framework",
]

ACTIVE_ROADMAP = [
    "Enumeração de subdomínios",
    "WhatWeb",
    "Wappalyzer / BuiltWith",
    "DotGit exposed",
    "Wafw00f",
    "Cabeçalhos HTTP",
    "Banner grabbing (nmap)",
    "Análise de código-fonte",
]


def build_parser():
    parser = argparse.ArgumentParser(
        prog="huginn",
        description="Huginn — ferramenta de reconhecimento passivo e ativo para pentest.",
    )
    parser.add_argument("-d", "--domain", required=True, help="Domínio alvo (ex: dominio.com.br)")
    parser.add_argument("--passive", action="store_true", help="Executa o reconhecimento passivo")
    parser.add_argument("--active", action="store_true", help="Executa o reconhecimento ativo")
    parser.add_argument("--all", action="store_true", help="Executa passivo e ativo")
    parser.add_argument("--version", action="version", version=f"huginn {__version__}")
    return parser


def run_passive(domain, output_dir):
    logger.info(f"Reconhecimento passivo em {domain} — módulos ainda não implementados (Fase 2):")
    for item in PASSIVE_ROADMAP:
        logger.info(f"    [ ] {item}")


def run_active(domain, output_dir):
    logger.info(f"Reconhecimento ativo em {domain} — módulos ainda não implementados (Fase 3):")
    for item in ACTIVE_ROADMAP:
        logger.info(f"    [ ] {item}")


def main(argv=None):
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
