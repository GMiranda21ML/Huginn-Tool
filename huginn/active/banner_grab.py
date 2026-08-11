from huginn.core import logger, shell


def run(domain, output_dir):
    logger.info(f"Executando nmap (top 1000 portas, detecção de serviço/banner) em {domain}...")
    result_path = output_dir / "nmap.txt"
    xml_path = output_dir / "nmap.xml"

    returncode, _ = shell.run(
        [
            "nmap",
            "-sV",
            "-Pn",
            "--host-timeout",
            "5m",
            "-oN",
            str(result_path),
            "-oX",
            str(xml_path),
            domain,
        ]
    )

    if returncode != 0:
        logger.warn("nmap retornou erro.")
        return {"ok": False}

    logger.ok(f"nmap salvo em {result_path} (e XML em {xml_path})")
    return {"ok": True, "raw_file": str(result_path), "xml_file": str(xml_path)}
