import html
from datetime import datetime

from huginn import __version__

PREVIEW_LIMIT = 50

FONT_STACK = "'Liberation Sans', 'Noto Sans', 'DejaVu Sans', sans-serif"
MONO_STACK = "'Liberation Mono', 'Noto Sans Mono', 'DejaVu Sans Mono', monospace"

SEVERITY_COLORS = {
    "Critical": "#b91c1c",
    "High": "#c2410c",
    "Medium": "#b45309",
    "Low": "#4d7c0f",
}

ACCENT = "#4338ca"
ACCENT_LIGHT = "#818cf8"
INK = "#0f172a"

CSS = f"""
@page {{
    size: A4;
    margin: 2.4cm 1.8cm 2cm 1.8cm;
    @bottom-center {{
        content: "Huginn — Relatório de Reconhecimento • página " counter(page) " de " counter(pages);
        font-size: 8px;
        color: #94a3b8;
        font-family: {FONT_STACK};
    }}
}}
@page:first {{
    margin: 0;
}}
* {{ box-sizing: border-box; }}
body {{
    font-family: {FONT_STACK};
    color: #1f2937;
    font-size: 10.5px;
    line-height: 1.55;
}}
.cover {{
    background: {INK};
    color: #f8fafc;
    width: 100%;
    height: 29.7cm;
    text-align: center;
    padding-top: 9cm;
    position: relative;
}}
.cover-title {{
    font-size: 52px;
    font-weight: 700;
    letter-spacing: 6px;
    color: {ACCENT_LIGHT};
}}
.cover-rule {{
    width: 3cm;
    height: 2px;
    background: {ACCENT_LIGHT};
    margin: 0.5cm auto 0.5cm auto;
    opacity: 0.6;
}}
.cover-subtitle {{
    font-size: 15px;
    color: #cbd5e1;
    margin-top: 0.2cm;
}}
.cover-tagline {{
    font-size: 10px;
    color: #64748b;
    font-style: italic;
    margin-top: 0.3cm;
}}
.cover-domain {{
    font-size: 26px;
    font-weight: 600;
    margin-top: 2.5cm;
    color: #f8fafc;
}}
.cover-date {{
    font-size: 10.5px;
    color: #94a3b8;
    margin-top: 0.3cm;
}}
.cover-classification {{
    position: absolute;
    bottom: 1.5cm;
    left: 0;
    right: 0;
    text-align: center;
    font-size: 8.5px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #475569;
}}
.section {{
    margin-bottom: 0.9cm;
}}
.section > h2 {{
    font-size: 15px;
    color: {INK};
    border-bottom: 2px solid {ACCENT};
    padding-bottom: 0.15cm;
    margin-bottom: 0.4cm;
    page-break-after: avoid;
}}
h3 {{
    font-size: 11.5px;
    color: {INK};
    margin: 0.5cm 0 0.15cm 0;
    padding-left: 0.22cm;
    border-left: 3px solid {ACCENT};
    page-break-after: avoid;
}}
h4 {{
    font-size: 10px;
    color: #334155;
    margin: 0.3cm 0 0.1cm 0;
    page-break-after: avoid;
}}
p {{ margin: 0.1cm 0; }}
ul {{ margin: 0.1cm 0 0.3cm 0; padding-left: 0.5cm; }}
li {{ margin-bottom: 0.05cm; }}
a {{ color: {ACCENT}; text-decoration: none; word-break: break-all; }}
.muted {{ color: #6b7280; font-style: italic; }}
pre {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-left: 3px solid #cbd5e1;
    border-radius: 4px;
    padding: 0.25cm 0.35cm;
    font-family: {MONO_STACK};
    font-size: 8.5px;
    white-space: pre-wrap;
    word-break: break-all;
    color: {INK};
}}
.mono-list {{
    font-family: {MONO_STACK};
    font-size: 9px;
    list-style: none;
    padding-left: 0;
}}
.chips {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.14cm;
    margin: 0.1cm 0 0.3cm 0;
}}
.chip {{
    display: inline-block;
    background: #eef2ff;
    color: {ACCENT};
    border: 1px solid #e0e7ff;
    border-radius: 3px;
    padding: 0.07cm 0.2cm;
    font-family: {MONO_STACK};
    font-size: 8.5px;
    white-space: nowrap;
}}
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 0.15cm 0 0.35cm 0;
    font-size: 8.5px;
}}
table th, table td {{
    border: 1px solid #e2e8f0;
    padding: 0.12cm 0.18cm;
    text-align: left;
    vertical-align: top;
}}
table thead th {{
    background: #eef2ff;
    color: {ACCENT};
    font-weight: 700;
}}
table tbody tr:nth-child(even) {{ background: #f8fafc; }}
.stats {{
    display: flex;
    gap: 0.4cm;
    margin-bottom: 0.3cm;
}}
.stat {{
    flex: 1;
    text-align: center;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-top: 3px solid {ACCENT};
    border-radius: 4px;
    padding: 0.35cm 0;
}}
.stat-value {{
    font-size: 22px;
    font-weight: 700;
    color: {INK};
}}
.stat-label {{
    font-size: 8.5px;
    color: #6b7280;
    margin-top: 0.1cm;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}
.finding {{
    border-left: 5px solid #6b7280;
    background: #f8fafc;
    border-radius: 4px;
    padding: 0.3cm 0.4cm;
    margin-bottom: 0.35cm;
    page-break-inside: avoid;
}}
.finding-header {{
    display: flex;
    align-items: center;
    gap: 0.3cm;
    margin-bottom: 0.15cm;
}}
.finding-header h3 {{ margin: 0; border-left: none; padding-left: 0; }}
.badge {{
    color: #fff;
    font-size: 8.5px;
    font-weight: 700;
    border-radius: 10px;
    padding: 0.09cm 0.28cm;
    white-space: nowrap;
}}
.vector code {{
    font-family: {MONO_STACK};
    font-size: 8.5px;
    background: #e2e8f0;
    padding: 0.02cm 0.12cm;
    border-radius: 3px;
}}
.footer-note {{
    text-align: center;
    color: #94a3b8;
    font-size: 9px;
    margin-top: 1cm;
}}
"""


def _esc(value):
    if value is None:
        return ""
    return html.escape(str(value))


def _pre(text):
    if not text or not str(text).strip():
        return "<p class='muted'>Sem dados coletados.</p>"
    return f"<pre>{_esc(text)}</pre>"


def _chip_list(items):
    if not items:
        return "<p class='muted'>Nenhum encontrado.</p>"
    return "<div class='chips'>" + "".join(f"<span class='chip'>{_esc(item)}</span>" for item in items) + "</div>"


def _chip_links(entries):
    if not entries:
        return "<p class='muted'>Nenhum encontrado.</p>"
    chips = "".join(f"<a class='chip' href='{_esc(url)}'>{_esc(label)}</a>" for label, url in entries)
    return f"<div class='chips'>{chips}</div>"


def _lines_preview(text, limit=PREVIEW_LIMIT):
    if not text or not str(text).strip():
        return "<p class='muted'>Sem dados coletados.</p>"
    lines = [line for line in text.splitlines() if line.strip()]
    shown = lines[:limit]
    out = _chip_list(shown)
    if len(lines) > limit:
        out += f"<p class='muted'>... e mais {len(lines) - limit} (ver arquivo completo em output/&lt;domínio&gt;/).</p>"
    return out


def _section(title, body):
    return f"<section class='section'><h2>{_esc(title)}</h2>{body}</section>"


def _stat_tile(label, value):
    return f"<div class='stat'><div class='stat-value'>{_esc(value)}</div><div class='stat-label'>{_esc(label)}</div></div>"


def _finding_card(finding):
    color = SEVERITY_COLORS.get(finding["severity"], "#6b7280")
    return (
        f"<div class='finding' style='border-left-color:{color}'>"
        f"<div class='finding-header'>"
        f"<span class='badge' style='background:{color}'>{_esc(finding['severity'])} — {finding['score']}</span>"
        f"<h3>{_esc(finding['title'])}</h3>"
        f"</div>"
        f"<p>{_esc(finding['description'])}</p>"
        f"<p class='vector'>Vetor CVSS 3.1: <code>{_esc(finding['vector'])}</code></p>"
        f"</div>"
    )


def _render_wayback(wb):
    if not wb:
        return "<p class='muted'>Não coletado.</p>"
    first = wb.get("first") or "?"
    last = wb.get("last") or "?"
    return f"<p><strong>Primeiro snapshot:</strong> {_esc(first)} &nbsp;&nbsp; <strong>Último snapshot:</strong> {_esc(last)}</p>"


def _banner_summary(ip_info):
    banners = ip_info.get("banners") or {}
    bits = []
    for proto in ("http", "https"):
        b = banners.get(proto)
        if not b:
            continue
        if b.get("server"):
            bits.append(b["server"])
        for app in b.get("apps") or []:
            bits.append(app)
    ssh = banners.get("ssh")
    if ssh and ssh.get("banner"):
        bits.append(ssh["banner"])
    seen = []
    for bit in bits:
        if bit not in seen:
            seen.append(bit)
    return ", ".join(seen)


def _dns_record_rows(records):
    rows = []
    for rec in records[:PREVIEW_LIMIT]:
        host = rec.get("host", "")
        ips = rec.get("ips") or [{}]
        for ip_info in ips:
            rows.append(
                "<tr>"
                f"<td>{_esc(host)}</td>"
                f"<td>{_esc(ip_info.get('ip'))}</td>"
                f"<td>{_esc(ip_info.get('country_code') or ip_info.get('country'))}</td>"
                f"<td>{_esc(ip_info.get('asn_name'))}</td>"
                f"<td>{_esc(_banner_summary(ip_info))}</td>"
                "</tr>"
            )
    return "".join(rows)


def _dns_table(title, records):
    if not records:
        return f"<h4>{title} (0)</h4><p class='muted'>Nenhum registro encontrado.</p>"
    rows = _dns_record_rows(records)
    table = (
        "<table><thead><tr><th>Host</th><th>IP</th><th>País</th><th>ASN / Provedor</th><th>Banner / Tecnologia</th></tr></thead>"
        f"<tbody>{rows}</tbody></table>"
    )
    return f"<h4>{title} ({len(records)})</h4>{table}"


def _render_dnsdumpster(dd):
    if dd is None:
        return "<p class='muted'>Não coletado (sem HUGINN_DNSDUMPSTER_API_KEY configurada, ou módulo não executado).</p>"
    if isinstance(dd, dict) and dd.get("error"):
        return f"<p class='muted'>Erro na consulta: {_esc(dd['error'])}</p>"

    parts = [_dns_table("Registros A", dd.get("a") or [])]

    total_a = dd.get("total_a_recs")
    a_shown = len(dd.get("a") or [])
    if total_a and total_a > a_shown:
        parts.append(f"<p class='muted'>... e mais {total_a - a_shown} registros A (limite do plano gratuito da API DNSDumpster).</p>")

    cnames = dd.get("cname") or []
    if cnames:
        parts.append(_dns_table("Registros CNAME", cnames))

    parts.append(_dns_table("Registros MX", dd.get("mx") or []))
    parts.append(_dns_table("Servidores NS", dd.get("ns") or []))

    txt = dd.get("txt") or []
    parts.append(f"<h4>Registros TXT ({len(txt)})</h4>")
    if txt:
        items = "".join(f"<li>{_esc(t)}</li>" for t in txt[:PREVIEW_LIMIT])
        parts.append(f"<ul class='mono-list'>{items}</ul>")
    else:
        parts.append("<p class='muted'>Nenhum registro encontrado.</p>")

    return "".join(parts)


def _render_github(gh):
    if not gh:
        return "<p class='muted'>Não coletado.</p>"

    parts = []
    org = gh.get("org")
    if org:
        parts.append(f"<p><strong>Organização encontrada:</strong> <a href='{_esc(org.get('html_url'))}'>{_esc(org.get('html_url'))}</a></p>")
    else:
        parts.append("<p class='muted'>Nenhuma organização correspondente encontrada.</p>")

    repos = gh.get("repositories") or []
    parts.append(f"<h4>Repositórios públicos ({len(repos)})</h4>")
    if repos:
        rows = "".join(
            f"<tr><td><a href='{_esc(r.get('html_url'))}'>{_esc(r.get('full_name'))}</a></td>"
            f"<td>{_esc(r.get('description') or '')}</td>"
            f"<td>{_esc(r.get('stargazers_count', ''))}</td></tr>"
            for r in repos[:PREVIEW_LIMIT]
        )
        parts.append(f"<table><thead><tr><th>Repositório</th><th>Descrição</th><th>★</th></tr></thead><tbody>{rows}</tbody></table>")
    else:
        parts.append("<p class='muted'>Nenhum repositório encontrado.</p>")

    orgs = gh.get("orgs_search") or []
    parts.append(f"<h4>Organizações relacionadas ({len(orgs)})</h4>")
    parts.append(_chip_links([(o.get("login"), o.get("html_url")) for o in orgs[:PREVIEW_LIMIT]]))

    code = gh.get("code_search") or {}
    if code.get("skipped"):
        parts.append("<p class='muted'>Busca de código não realizada (sem HUGINN_GITHUB_TOKEN configurado).</p>")
    elif code.get("items"):
        items_c = code["items"]
        parts.append(f"<h4>Código público mencionando o domínio ({len(items_c)})</h4>")
        rows = "".join(
            f"<tr><td>{_esc(i.get('repository', {}).get('full_name'))}</td><td>{_esc(i.get('path'))}</td></tr>"
            for i in items_c[:PREVIEW_LIMIT]
        )
        parts.append(f"<table><thead><tr><th>Repositório</th><th>Arquivo</th></tr></thead><tbody>{rows}</tbody></table>")

    return "".join(parts)


def _render_links(links):
    if not links:
        return "<p class='muted'>Não coletado.</p>"

    parts = []
    google = links.get("google_hacking")
    if google:
        items = "".join(f"<li>{_esc(g['descricao'])}: <a href='{_esc(g['url'])}'>{_esc(g['url'])}</a></li>" for g in google)
        parts.append(f"<h4>Google Hacking</h4><ul>{items}</ul>")
    if links.get("dorksearch"):
        parts.append(f"<p><strong>dorksearch.com:</strong> <a href='{_esc(links['dorksearch'])}'>{_esc(links['dorksearch'])}</a></p>")

    for key, label in (
        ("metacrawler", "MetaCrawler"),
        ("linkedin", "LinkedIn"),
        ("osint_framework", "OSINT Framework"),
        ("netcraft", "Netcraft"),
        ("builtwith", "BuiltWith"),
    ):
        entry = links.get(key)
        if entry and entry.get("url"):
            parts.append(f"<p><strong>{label}:</strong> <a href='{_esc(entry['url'])}'>{_esc(entry['url'])}</a></p>")

    wap = links.get("wappalyzer")
    if wap:
        parts.append(f"<p><strong>Wappalyzer:</strong> {_esc(wap.get('nota'))}</p>")

    return "".join(parts) if parts else "<p class='muted'>Sem dados coletados.</p>"


def _render_dotgit(dg):
    if not dg:
        return "<p class='muted'>Não coletado.</p>"
    if dg.get("exposed"):
        return f"<p style='color:#b91c1c'><strong>EXPOSTO</strong> — HTTP {_esc(dg.get('status_code'))} em {_esc(dg.get('url'))}. Ver achado no início do relatório.</p>"
    return f"<p>Não exposto (HTTP {_esc(dg.get('status_code'))}).</p>"


def _render_headers(h):
    if not h or not h.get("raw"):
        return "<p class='muted'>Não coletado.</p>"
    missing = h.get("missing_headers") or []
    parts = []
    if missing:
        parts.append(f"<p style='color:#b45309'><strong>Ausentes:</strong> {_esc(', '.join(missing))} — ver achado no início do relatório.</p>")
    else:
        parts.append("<p>Todos os headers de segurança verificados estão presentes.</p>")
    parts.append(_pre(h["raw"]))
    return "".join(parts)


def _render_source(sa):
    if not sa:
        return "<p class='muted'>Não coletado.</p>"
    parts = []
    generator = sa.get("generator")
    parts.append(f"<p><strong>Meta generator:</strong> {_esc(generator) if generator else 'não encontrado'}</p>")
    domains = sa.get("external_domains") or []
    parts.append(f"<h4>Domínios externos referenciados ({len(domains)})</h4>")
    parts.append(_chip_list(domains[:PREVIEW_LIMIT]))
    return "".join(parts)


def build_html(domain, data, findings):
    generated_at = datetime.now().strftime("%d/%m/%Y %H:%M")
    passive = data["passive"]
    active = data["active"]

    subdomains_raw = (active.get("subdomains") or {}).get("raw")
    subdomains_count = len([line for line in subdomains_raw.splitlines() if line.strip()]) if subdomains_raw else 0
    repos_count = len((passive.get("github") or {}).get("repositories") or [])

    severity_counts = {}
    for finding in findings:
        severity_counts[finding["severity"]] = severity_counts.get(finding["severity"], 0) + 1
    severity_summary = " · ".join(f"{count} {sev}" for sev, count in severity_counts.items()) or "Nenhum achado com CVSS calculado nesta coleta."

    findings_html = "".join(_finding_card(f) for f in findings) if findings else "<p class='muted'>Nenhum achado com severidade calculada nesta coleta.</p>"

    summary_html = (
        "<div class='stats'>"
        + _stat_tile("Subdomínios encontrados", subdomains_count)
        + _stat_tile("Repositórios no GitHub", repos_count)
        + _stat_tile("Achados", len(findings))
        + "</div>"
        + f"<p class='muted'>{_esc(severity_summary)}</p>"
    )

    passive_parts = [
        f"<h3>Whois</h3>{_pre((passive.get('whois') or {}).get('raw'))}",
        f"<h3>Wayback Machine</h3>{_render_wayback(passive.get('wayback'))}",
        f"<h3>DNSDumpster</h3>{_render_dnsdumpster(passive.get('dnsdumpster'))}",
        f"<h3>GitHub</h3>{_render_github(passive.get('github'))}",
        f"<h3>Dorks e links manuais</h3>{_render_links(passive.get('manual_links'))}",
    ]

    active_parts = [
        f"<h3>Subdomínios (subfinder)</h3>{_lines_preview((active.get('subdomains') or {}).get('raw'))}",
        f"<h3>WhatWeb</h3>{_pre((active.get('whatweb') or {}).get('raw'))}",
        f"<h3>BuiltWith / Wappalyzer</h3>{_render_links(active.get('manual_links'))}",
        f"<h3>DotGit</h3>{_render_dotgit(active.get('dotgit'))}",
        f"<h3>WAF (wafw00f)</h3>{_pre((active.get('wafw00f') or {}).get('raw'))}",
        f"<h3>Cabeçalhos HTTP</h3>{_render_headers(active.get('headers'))}",
        f"<h3>Nmap (banner grabbing)</h3>{_pre((active.get('nmap') or {}).get('raw'))}",
        f"<h3>Análise de código-fonte</h3>{_render_source(active.get('source_analysis'))}",
    ]

    body = (
        "<div class='cover'>"
        "<div class='cover-title'>HUGINN</div>"
        "<div class='cover-rule'></div>"
        "<div class='cover-subtitle'>Relatório de Reconhecimento</div>"
        "<div class='cover-tagline'>O corvo que observa e retorna com o relatório.</div>"
        f"<div class='cover-domain'>{_esc(domain)}</div>"
        f"<div class='cover-date'>Gerado em {_esc(generated_at)}</div>"
        "<div class='cover-classification'>Confidencial — uso restrito a testes autorizados</div>"
        "</div>"
        + _section("Resumo executivo", summary_html)
        + _section("Achados", findings_html)
        + _section("Reconhecimento passivo", "".join(passive_parts))
        + _section("Reconhecimento ativo", "".join(active_parts))
        + f"<div class='footer-note'>Gerado por Huginn v{_esc(__version__)} — uso restrito a testes autorizados.</div>"
    )

    return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"
