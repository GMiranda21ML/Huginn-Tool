from cvss import CVSS3

DOTGIT_VECTOR = "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N"
MISSING_HEADERS_VECTOR = "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:N"


def _score(vector):
    c = CVSS3(vector)
    return c.base_score, c.severities()[0]


def build_findings(data):
    findings = []

    dotgit = data["active"].get("dotgit")
    if dotgit and dotgit.get("exposed"):
        score, severity = _score(DOTGIT_VECTOR)
        findings.append({
            "title": "Diretório .git exposto",
            "description": (
                f"O diretório .git está publicamente acessível em {dotgit.get('url')}. "
                "Isso permite reconstruir o histórico de commits e potencialmente extrair "
                "código-fonte, credenciais e outros segredos versionados no repositório."
            ),
            "vector": DOTGIT_VECTOR,
            "score": score,
            "severity": severity,
        })

    headers = data["active"].get("headers") or {}
    missing = headers.get("missing_headers") or []
    if missing:
        score, severity = _score(MISSING_HEADERS_VECTOR)
        findings.append({
            "title": "Headers de segurança ausentes",
            "description": (
                "Os seguintes headers de segurança não foram encontrados na resposta HTTP: "
                f"{', '.join(missing)}. A ausência desses headers facilita ataques como "
                "clickjacking, XSS e MIME sniffing. Classificação heurística por categoria "
                "de achado, sem CVE associado."
            ),
            "vector": MISSING_HEADERS_VECTOR,
            "score": score,
            "severity": severity,
        })

    findings.sort(key=lambda f: f["score"], reverse=True)
    return findings
