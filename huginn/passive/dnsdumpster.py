import json

from huginn.core import config, logger, shell

API_URL = "https://api.dnsdumpster.com/domain/{domain}"


def run(domain, output_dir):
    api_key = config.get("HUGINN_DNSDUMPSTER_API_KEY")
    if not api_key:
        logger.warn("HUGINN_DNSDUMPSTER_API_KEY não configurada — pulando DNSDumpster.")
        logger.warn("Gere uma chave gratuita em https://dnsdumpster.com/ e adicione ao .env (veja .env.example).")
        return {"ok": False, "skipped": True}

    logger.info(f"Consultando DNSDumpster (API oficial) para {domain}...")
    url = API_URL.format(domain=domain)
    returncode, out, err = shell.capture(
        ["curl", "-fsSL", "--max-time", "40", "-H", f"X-API-Key: {api_key}", url]
    )
    result_path = output_dir / "dnsdumpster.json"
    result_path.write_text(out)

    if returncode != 0 or not out.strip():
        logger.warn(f"Falha ao consultar DNSDumpster: {err.strip()}")
        return {"ok": False}

    data = json.loads(out)
    if isinstance(data, dict) and "error" in data:
        logger.warn(f"DNSDumpster retornou erro: {data['error']}")
        return {"ok": False, "error": data["error"]}

    logger.ok(f"DNSDumpster: resposta salva em {result_path}")
    return {"ok": True, "raw_file": str(result_path)}
