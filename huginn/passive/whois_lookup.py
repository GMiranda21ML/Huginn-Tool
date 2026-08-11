from huginn.core import logger, shell


def run(domain, output_dir):
    logger.info(f"Consultando WHOIS de {domain}...")
    returncode, raw = shell.run(["whois", domain])
    result_path = output_dir / "whois.txt"
    result_path.write_text(raw)
    if returncode != 0 or not raw.strip():
        logger.warn("Consulta WHOIS não retornou dados.")
        return {"ok": False}
    logger.ok(f"WHOIS salvo em {result_path}")
    return {"ok": True, "raw_file": str(result_path)}
