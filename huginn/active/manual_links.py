import json

from huginn.core import logger


def build_links(domain):
    return {
        "builtwith": {"url": f"https://builtwith.com/{domain}"},
        "wappalyzer": {"nota": "Sem CLI nativa no Linux; use a extensão do navegador para complementar o WhatWeb."},
    }


def run(domain, output_dir):
    logger.info("Gerando link do BuiltWith (Wappalyzer não tem CLI nativa; WhatWeb já cobre o fingerprint automatizado)...")
    data = build_links(domain)
    result_path = output_dir / "manual_links.json"
    result_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    logger.info(f"    [builtwith] {data['builtwith']['url']}")
    logger.info(f"    [wappalyzer] {data['wappalyzer']['nota']}")
    logger.ok(f"Link salvo em {result_path}")
    return {"ok": True, "raw_file": str(result_path)}
