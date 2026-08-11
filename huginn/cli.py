import argparse
import sys

from huginn import __version__
from huginn.core import banner, logger
from huginn.core.authorization import confirm_authorization
from huginn.core.output import prepare_output_dir
from huginn.passive import dnsdumpster, manual_links, wayback, whois_lookup

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
    passive_dir = output_dir / "passive"
    passive_dir.mkdir(parents=True, exist_ok=True)

    results = {}
    for name, module in (
        ("whois", whois_lookup),
        ("wayback", wayback),
        ("dnsdumpster", dnsdumpster),
        ("manual_links", manual_links),
    ):
        results[name] = module.run(domain, passive_dir)
    return results


def run_active(domain, output_dir):
    logger.info(f"Reconhecimento ativo em {domain} — módulos ainda não implementados (Fase 3):")
    for item in ACTIVE_ROADMAP:
        logger.info(f"    [ ] {item}")


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
