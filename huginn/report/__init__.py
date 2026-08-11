from huginn.report import collector, findings, pdf, render


def generate_report(domain, output_dir):
    data = collector.collect(output_dir)
    findings_list = findings.build_findings(data)
    html_string = render.build_html(domain, data, findings_list)

    report_path = output_dir / "relatorio.pdf"
    pdf.render_pdf(html_string, report_path)
    return report_path
