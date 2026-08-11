from huginn.core import logger, shell


def run(domain, output_dir):
    target = f"https://{domain}"
    logger.info(f"Executando WhatWeb em {target}...")
    returncode, raw = shell.run(["whatweb", "-a", "3", target])
    result_path = output_dir / "whatweb.txt"
    result_path.write_text(raw)

    if returncode != 0:
        logger.warn("WhatWeb retornou erro.")
        return {"ok": False, "raw_file": str(result_path)}

    logger.ok(f"WhatWeb salvo em {result_path}")
    return {"ok": True, "raw_file": str(result_path)}
