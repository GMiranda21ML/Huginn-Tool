from huginn.core import logger, shell

PREVIEW_LIMIT = 15


def run(domain, output_dir):
    logger.info(f"Enumerando subdomínios de {domain} (subfinder)...")
    returncode, out, err = shell.capture(["subfinder", "-d", domain, "-silent"])
    result_path = output_dir / "subdomains.txt"
    result_path.write_text(out)

    if returncode != 0:
        logger.warn(f"subfinder retornou erro: {err.strip()}")
        return {"ok": False}

    subdomains = [line.strip() for line in out.splitlines() if line.strip()]
    logger.ok(f"{len(subdomains)} subdomínios encontrados — salvos em {result_path}")
    for sub in subdomains[:PREVIEW_LIMIT]:
        logger.info(f"    {sub}")
    if len(subdomains) > PREVIEW_LIMIT:
        logger.info(f"    ... e mais {len(subdomains) - PREVIEW_LIMIT} (ver arquivo completo)")

    return {"ok": True, "count": len(subdomains), "subdomains": subdomains, "raw_file": str(result_path)}
