import json

from huginn.core import logger, shell

SECURITY_HEADERS = [
    "strict-transport-security",
    "content-security-policy",
    "x-frame-options",
    "x-content-type-options",
    "referrer-policy",
    "permissions-policy",
]


def _parse_last_header_block(raw):
    blocks = [b for b in raw.split("\r\n\r\n") if b.strip()]
    last_block = blocks[-1] if blocks else ""
    headers = {}
    for line in last_block.splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            headers[key.strip().lower()] = value.strip()
    return headers


def run(domain, output_dir):
    target = f"https://{domain}"
    logger.info(f"Coletando cabeçalhos HTTP de {target}...")
    returncode, raw, err = shell.capture(
        ["curl", "-s", "-D", "-", "-o", "/dev/null", "--max-time", "20", "-L", target]
    )
    result_path = output_dir / "headers.txt"
    result_path.write_text(raw)

    if returncode != 0 or not raw.strip():
        logger.warn(f"Falha ao coletar cabeçalhos: {err.strip()}")
        return {"ok": False}

    headers = _parse_last_header_block(raw)
    missing = [h for h in SECURITY_HEADERS if h not in headers]

    analysis_path = output_dir / "headers_analysis.json"
    analysis_path.write_text(json.dumps({"missing_headers": missing}, indent=2))

    if missing:
        logger.warn(f"Headers de segurança ausentes: {', '.join(missing)}")
    else:
        logger.ok("Todos os headers de segurança verificados estão presentes.")
    logger.ok(f"Headers salvos em {result_path}")

    return {"ok": True, "missing_headers": missing, "raw_file": str(result_path)}
