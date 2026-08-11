import json


def _read_text(path):
    if path.exists():
        return path.read_text()
    return None


def _read_json(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return None


def collect(output_dir):
    passive_dir = output_dir / "passive"
    active_dir = output_dir / "active"

    return {
        "passive": {
            "whois": {"raw": _read_text(passive_dir / "whois.txt")},
            "wayback": _read_json(passive_dir / "wayback.json"),
            "dnsdumpster": _read_json(passive_dir / "dnsdumpster.json"),
            "github": _read_json(passive_dir / "github.json"),
            "manual_links": _read_json(passive_dir / "manual_links.json"),
        },
        "active": {
            "subdomains": {"raw": _read_text(active_dir / "subdomains.txt")},
            "whatweb": {"raw": _read_text(active_dir / "whatweb.txt")},
            "manual_links": _read_json(active_dir / "manual_links.json"),
            "dotgit": _read_json(active_dir / "dotgit.json"),
            "wafw00f": {"raw": _read_text(active_dir / "wafw00f.txt")},
            "headers": {
                "raw": _read_text(active_dir / "headers.txt"),
                **(_read_json(active_dir / "headers_analysis.json") or {"missing_headers": []}),
            },
            "nmap": {"raw": _read_text(active_dir / "nmap.txt")},
            "source_analysis": _read_json(active_dir / "source_analysis.json"),
        },
    }
