import json
import re
from urllib.parse import quote

from huginn.core import config, logger, shell

API_BASE = "https://api.github.com"
PREVIEW_LIMIT = 10


def _slugify(domain):
    base = domain.split(".")[0]
    return re.sub(r"[^a-zA-Z0-9-]", "", base)


def _get(path, token):
    url = f"{API_BASE}{path}"
    cmd = ["curl", "-s", "--max-time", "20", "-H", "Accept: application/vnd.github+json"]
    if token:
        cmd += ["-H", f"Authorization: Bearer {token}"]
    cmd.append(url)

    returncode, out, err = shell.capture(cmd)
    if returncode != 0 or not out.strip():
        return None, err.strip() or "sem resposta da API do GitHub"

    try:
        data = json.loads(out)
    except json.JSONDecodeError:
        return None, "resposta inválida da API do GitHub"

    if isinstance(data, dict) and data.get("message"):
        msg = data["message"]
        if "rate limit" in msg.lower():
            return None, f"rate limit da API do GitHub excedido ({msg})"
        if msg == "Not Found":
            return {"not_found": True}, None
        return None, msg

    return data, None


def _check_org(slug, token):
    logger.info(f"Verificando organização no GitHub: {slug}...")
    data, err = _get(f"/orgs/{slug}", token)
    if err:
        logger.warn(f"Consulta de organização falhou: {err}")
        return None
    if data.get("not_found"):
        logger.info(f"Nenhuma organização '{slug}' encontrada no GitHub.")
        return None
    logger.ok(f"Organização encontrada: {data.get('html_url')}")
    return data


def _search_repositories(domain, token):
    logger.info(f"Buscando repositórios públicos que mencionam '{domain}'...")
    data, err = _get(f"/search/repositories?q={quote(domain)}", token)
    if err:
        logger.warn(f"Busca de repositórios falhou: {err}")
        return []

    items = data.get("items", [])
    logger.ok(f"{len(items)} repositório(s) encontrado(s) mencionando '{domain}'.")
    for repo in items[:PREVIEW_LIMIT]:
        logger.info(f"    {repo['full_name']} — {repo['html_url']}")
    return items


def _search_orgs(slug, token):
    logger.info(f"Buscando organizações no GitHub relacionadas a '{slug}'...")
    data, err = _get(f"/search/users?q={quote(slug)}+type:org", token)
    if err:
        logger.warn(f"Busca de organizações falhou: {err}")
        return []

    items = data.get("items", [])
    logger.ok(f"{len(items)} organização(ões) encontrada(s) relacionada(s) a '{slug}'.")
    for org in items[:PREVIEW_LIMIT]:
        logger.info(f"    {org['login']} — {org['html_url']}")
    return items


def _search_code(domain, token):
    if not token:
        logger.warn("Busca de código no GitHub exige autenticação — configure HUGINN_GITHUB_TOKEN no .env pra habilitar (opcional).")
        return {"ok": False, "skipped": True}

    logger.info(f"Buscando '{domain}' em código público no GitHub...")
    data, err = _get(f"/search/code?q={quote(domain)}", token)
    if err:
        logger.warn(f"Busca de código falhou: {err}")
        return {"ok": False}

    items = data.get("items", [])
    logger.ok(f"{len(items)} arquivo(s) encontrado(s) mencionando '{domain}' em código público.")
    for item in items[:PREVIEW_LIMIT]:
        logger.info(f"    {item['repository']['full_name']}: {item['path']}")
    return {"ok": True, "count": len(items), "items": items}


def run(domain, output_dir):
    token = config.get("HUGINN_GITHUB_TOKEN")
    if not token:
        logger.info("HUGINN_GITHUB_TOKEN não configurada — seguindo sem chave (repositórios/orgs funcionam, busca de código fica de fora).")

    slug = _slugify(domain)
    org = _check_org(slug, token)
    repositories = _search_repositories(domain, token)
    orgs = _search_orgs(slug, token)
    code = _search_code(domain, token)

    result = {
        "org": org,
        "repositories": repositories,
        "orgs_search": orgs,
        "code_search": code,
    }
    result_path = output_dir / "github.json"
    result_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    logger.ok(f"Resultado do GitHub salvo em {result_path}")

    return {"ok": True, "raw_file": str(result_path), **result}
