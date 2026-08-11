import json

from huginn.core import logger, shell

CDX_URL = "https://web.archive.org/cdx/search/cdx"


def _query(domain, limit):
    url = f"{CDX_URL}?url={domain}&output=json&fl=timestamp,original&limit={limit}"
    returncode, out, err = shell.capture(["curl", "-fsSL", "--max-time", "40", url])
    if returncode != 0:
        return None, err.strip() or f"curl saiu com código {returncode} (possível timeout)"
    if not out.strip():
        return None, "resposta vazia da CDX API"
    rows = json.loads(out)
    entry = rows[1] if len(rows) > 1 else None
    return entry, None if entry else "sem snapshots"


def run(domain, output_dir):
    logger.info(f"Consultando Wayback Machine (CDX API) para {domain}...")

    first_entry, first_err = _query(domain, 1)
    last_entry, last_err = _query(domain, -1)

    result_path = output_dir / "wayback.json"
    result_path.write_text(
        json.dumps({"first": first_entry, "last": last_entry}, indent=2, ensure_ascii=False)
    )

    if first_entry is None and last_entry is None:
        logger.warn(f"Nenhum snapshot encontrado no Wayback Machine (primeiro: {first_err}; último: {last_err}).")
        return {"ok": True, "count": 0, "raw_file": str(result_path)}

    if first_entry is None:
        logger.warn(f"Não foi possível obter o primeiro snapshot ({first_err}).")
    if last_entry is None:
        logger.warn(f"Não foi possível obter o último snapshot ({last_err}).")

    first_ts = first_entry[0] if first_entry else "?"
    last_ts = last_entry[0] if last_entry else "?"
    logger.ok(f"Wayback Machine — primeiro snapshot: {first_ts}, último snapshot: {last_ts}")
    return {
        "ok": True,
        "first": first_ts,
        "last": last_ts,
        "raw_file": str(result_path),
    }
