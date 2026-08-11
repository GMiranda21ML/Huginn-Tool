from huginn.core import logger, shell


def run(domain, output_dir):
    target = f"https://{domain}"
    logger.info(f"Detectando WAF em {target} (wafw00f)...")
    returncode, raw = shell.run(["wafw00f", "--no-colors", target])
    result_path = output_dir / "wafw00f.txt"
    result_path.write_text(raw)

    if returncode != 0:
        logger.warn("wafw00f retornou erro.")
        return {"ok": False, "raw_file": str(result_path)}

    logger.ok(f"wafw00f salvo em {result_path}")
    return {"ok": True, "raw_file": str(result_path)}
