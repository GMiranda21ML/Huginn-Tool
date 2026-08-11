import json

from huginn.core import logger, shell


def run(domain, output_dir):
    target = f"https://{domain}/.git/HEAD"
    logger.info(f"Verificando exposição de .git em {target}...")
    returncode, out, err = shell.capture(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", "20", target]
    )
    status = out.strip()
    exposed = status == "200"

    result_path = output_dir / "dotgit.json"
    result_path.write_text(json.dumps({"url": target, "status_code": status, "exposed": exposed}, indent=2))

    if returncode != 0 and not status:
        logger.warn(f"Falha ao verificar .git: {err.strip()}")
        return {"ok": False}

    if exposed:
        logger.err(f"CRÍTICO: .git exposto em {target} (HTTP {status})")
    else:
        logger.ok(f".git não exposto (HTTP {status})")

    return {"ok": True, "exposed": exposed, "status_code": status, "raw_file": str(result_path)}
