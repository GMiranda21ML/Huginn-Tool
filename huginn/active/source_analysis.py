import json
import re
from urllib.parse import urlparse

from huginn.core import logger, shell

GENERATOR_RE = re.compile(r'<meta[^>]+name=["\']generator["\'][^>]+content=["\']([^"\']+)["\']', re.IGNORECASE)
SRC_RE = re.compile(r'(?:src|href)=["\']([^"\']+)["\']', re.IGNORECASE)
PREVIEW_LIMIT = 15


def _extract_meta_generator(html):
    match = GENERATOR_RE.search(html)
    return match.group(1) if match else None


def _extract_external_domains(html, domain):
    domains = set()
    for match in SRC_RE.finditer(html):
        url = match.group(1)
        if url.startswith("//"):
            url = "https:" + url
        if not url.startswith("http"):
            continue
        host = urlparse(url).netloc
        if host and domain not in host:
            domains.add(host)
    return sorted(domains)


def run(domain, output_dir):
    target = f"https://{domain}"
    logger.info(f"Analisando código-fonte de {target}...")
    returncode, html, err = shell.capture(["curl", "-fsSL", "--max-time", "20", "-L", target])
    result_path = output_dir / "source_analysis.json"

    if returncode != 0 or not html.strip():
        logger.warn(f"Falha ao obter o HTML: {err.strip()}")
        result_path.write_text(json.dumps({"ok": False, "error": err.strip()}))
        return {"ok": False}

    generator = _extract_meta_generator(html)
    external_domains = _extract_external_domains(html, domain)
    result_path.write_text(
        json.dumps({"generator": generator, "external_domains": external_domains}, indent=2, ensure_ascii=False)
    )

    if generator:
        logger.ok(f"Meta generator encontrado: {generator}")
    else:
        logger.info("Nenhuma tag <meta name=generator> encontrada.")

    logger.ok(f"{len(external_domains)} domínios externos referenciados (scripts/links) — salvos em {result_path}")
    for host in external_domains[:PREVIEW_LIMIT]:
        logger.info(f"    {host}")
    if len(external_domains) > PREVIEW_LIMIT:
        logger.info(f"    ... e mais {len(external_domains) - PREVIEW_LIMIT} (ver arquivo completo)")

    return {"ok": True, "generator": generator, "external_domains": external_domains, "raw_file": str(result_path)}
