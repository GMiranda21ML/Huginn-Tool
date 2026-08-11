from weasyprint import HTML


def render_pdf(html_string, output_path):
    HTML(string=html_string).write_pdf(str(output_path))
