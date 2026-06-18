"""
Exporta relatorio/relatorio.md para PDF.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RELATORIO_MD = ROOT / "relatorio" / "relatorio.md"
RELATORIO_PDF = ROOT / "relatorio" / "relatorio.pdf"
IMG_DIR = ROOT / "relatorio" / "imagens"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"/>
<style>
  @page {{ size: A4; margin: 2cm; }}
  body {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 11pt; line-height: 1.5; color: #1a1a1a; }}
  h1 {{ font-size: 20pt; border-bottom: 2px solid #e63946; padding-bottom: 6px; }}
  h2 {{ font-size: 14pt; color: #333; margin-top: 24px; }}
  h3 {{ font-size: 12pt; color: #555; }}
  table {{ border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 10pt; }}
  th, td {{ border: 1px solid #ccc; padding: 6px 8px; text-align: left; }}
  th {{ background: #f0f0f0; }}
  code {{ background: #f4f4f4; padding: 1px 4px; font-size: 9pt; }}
  pre {{ background: #f4f4f4; padding: 12px; font-size: 8.5pt; overflow-wrap: break-word; white-space: pre-wrap; }}
  img {{ max-width: 100%; margin: 12px 0; }}
  em {{ color: #555; font-size: 10pt; }}
  hr {{ border: none; border-top: 1px solid #ddd; margin: 24px 0; }}
</style>
</head>
<body>
{body}
</body>
</html>
"""


def md_to_html(md_text: str, base_dir: Path) -> str:
    import base64
    import markdown

    def replace_img(match: re.Match) -> str:
        alt, src = match.group(1), match.group(2)
        img_path = (base_dir / src).resolve()
        if img_path.exists():
            mime = "image/png" if img_path.suffix.lower() == ".png" else "image/jpeg"
            b64 = base64.b64encode(img_path.read_bytes()).decode("ascii")
            return f'<img src="data:{mime};base64,{b64}" alt="{alt}"/>'
        return match.group(0)

    md_text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", replace_img, md_text)
    body = markdown.markdown(md_text, extensions=["tables", "fenced_code", "nl2br"])
    return HTML_TEMPLATE.format(body=body)


def export_pdf() -> None:
    if not RELATORIO_MD.exists():
        raise FileNotFoundError(f"Relatório não encontrado: {RELATORIO_MD}")

    md_text = RELATORIO_MD.read_text(encoding="utf-8")
    html = md_to_html(md_text, RELATORIO_MD.parent)

    try:
        from weasyprint import HTML
        HTML(string=html, base_url=str(RELATORIO_MD.parent)).write_pdf(str(RELATORIO_PDF))
    except ImportError:
        from xhtml2pdf import pisa
        with open(RELATORIO_PDF, "wb") as pdf_file:
            status = pisa.CreatePDF(html, dest=pdf_file, encoding="utf-8")
        if status.err:
            raise RuntimeError("Falha ao gerar PDF com xhtml2pdf")

    print(f"PDF gerado em {RELATORIO_PDF}")


def main() -> None:
    export_pdf()


if __name__ == "__main__":
    main()
