import json
from urllib.parse import quote

from huginn.core import logger

DORKS = [
    ("Subdomínios indexados", "site:*.{domain}"),
    ("Domínio raiz indexado", "site:{domain}"),
    ("Arquivos sensíveis", "site:{domain} (filetype:pdf OR filetype:xlsx OR filetype:bkp)"),
    ("E-mails expostos", '"@{domain}"'),
    ("Cache do Google", "cache:{domain}"),
]


def build_links(domain):
    dorks = [(desc, template.format(domain=domain)) for desc, template in DORKS]
    google_links = [
        {"descricao": desc, "dork": dork, "url": f"https://www.google.com/search?q={quote(dork)}"}
        for desc, dork in dorks
    ]
    dorksearch_url = f"https://dorksearch.com/?q={quote(' | '.join(dork for _, dork in dorks))}"

    return {
        "google_hacking": google_links,
        "dorksearch": dorksearch_url,
        "metacrawler": {"url": "https://www.metacrawler.com/", "busque_por": domain},
        "linkedin": {"url": f"https://www.linkedin.com/search/results/companies/?keywords={quote(domain)}"},
        "osint_framework": {"url": "https://osintframework.com/"},
        "netcraft": {"url": f"https://sitereport.netcraft.com/?url={quote(domain)}"},
    }


def run(domain, output_dir):
    logger.info("Gerando dorks e links de OSINT manual (sem scraping)...")
    data = build_links(domain)
    result_path = output_dir / "manual_links.json"
    result_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    for item in data["google_hacking"]:
        logger.info(f"    [google] {item['descricao']}: {item['url']}")
    logger.info(f"    [dorksearch] {data['dorksearch']}")
    logger.info(f"    [metacrawler] {data['metacrawler']['url']} (busque por: {domain})")
    logger.info(f"    [linkedin] {data['linkedin']['url']}")
    logger.info(f"    [osint framework] {data['osint_framework']['url']}")
    logger.info(f"    [netcraft] {data['netcraft']['url']}")
    logger.ok(f"Links salvos em {result_path}")
    return {"ok": True, "raw_file": str(result_path)}
