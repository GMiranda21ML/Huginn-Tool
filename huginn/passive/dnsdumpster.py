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
        ["curl", "-sSL", "--max-time", "40", "-H", f"X-API-Key: {api_key}", url]
    )

    if returncode != 0 or not out.strip():
        logger.warn(f"Falha ao consultar DNSDumpster: {err.strip() or 'sem resposta'}")
        return {"ok": False}

    try:
        data = json.loads(out)
    except json.JSONDecodeError:
        logger.warn("DNSDumpster retornou uma resposta inválida (não é JSON).")
        return {"ok": False}

    result_path = output_dir / "dnsdumpster.json"

    if isinstance(data, dict) and "error" in data:
        logger.warn(f"DNSDumpster retornou erro: {data['error']}")
        result_path.write_text(out)
        return {"ok": False, "error": data["error"]}

    result_path.write_text(out)
    logger.ok(f"DNSDumpster: resposta salva em {result_path}")
    return {"ok": True, "raw_file": str(result_path)}
