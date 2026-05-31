"""Generate JARVIS AI Product Report PDF from PRODUCT_GUIDE.md."""

import re
import sys
from pathlib import Path

from fpdf import FPDF

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCE = PROJECT_ROOT / "PRODUCT_GUIDE.md"
OUTPUT = PROJECT_ROOT / "JARVIS_AI_Product_Report.pdf"


class ReportPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 9)
            self.set_text_color(100, 100, 100)
            self.cell(0, 8, clean_text("JARVIS AI - Product Guide & Final Report"), align="C", new_x="LMARGIN", new_y="NEXT")
            self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


def clean_text(text: str) -> str:
    replacements = {
        "\u2014": "-", "\u2013": "-", "\u201c": '"', "\u201d": '"',
        "\u2018": "'", "\u2019": "'", "\u2022": "*", "\u2192": "->",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text.encode("latin-1", errors="replace").decode("latin-1")


def add_wrapped(pdf: ReportPDF, text: str, size: int = 10, style: str = "") -> None:
    pdf.set_font("Helvetica", style, size)
    pdf.set_text_color(30, 30, 30)
    pdf.multi_cell(0, 5.5, clean_text(text))
    pdf.ln(2)


def parse_table(lines: list[str]) -> list[list[str]]:
    rows = []
    for line in lines:
        if not line.strip().startswith("|"):
            break
        if re.match(r"^\|\s*-+", line):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        rows.append(cells)
    return rows


def render_table(pdf: ReportPDF, rows: list[list[str]]) -> None:
    if not rows:
        return
    col_count = len(rows[0])
    page_width = pdf.w - pdf.l_margin - pdf.r_margin
    col_width = page_width / col_count

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(240, 240, 240)
    for i, cell in enumerate(rows[0]):
        pdf.cell(col_width, 7, clean_text(cell)[:40], border=1, fill=True)
    pdf.ln()

    pdf.set_font("Helvetica", "", 9)
    for row in rows[1:]:
        if pdf.get_y() > 270:
            pdf.add_page()
        for i, cell in enumerate(row):
            pdf.cell(col_width, 6, clean_text(cell)[:45], border=1)
        pdf.ln()
    pdf.ln(3)


def build_pdf() -> None:
    if not SOURCE.exists():
        print(f"Source not found: {SOURCE}")
        sys.exit(1)

    content = SOURCE.read_text(encoding="utf-8")
    lines = content.splitlines()

    pdf = ReportPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # Title page
    pdf.ln(40)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(20, 60, 120)
    pdf.cell(0, 14, clean_text("JARVIS AI"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Helvetica", "", 16)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 10, "Complete Product Guide & Final Report", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, "Telegram-First Remote Productivity Assistant", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Platform: Windows 10/11", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Author: Manikandan K", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "License: MIT | Status: Production-ready", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(30)
    pdf.set_font("Helvetica", "I", 11)
    pdf.cell(0, 8, clean_text("Version 1.0 - Product Release"), align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.add_page()
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()

        if line.startswith("# ") and not line.startswith("## "):
            i += 1
            continue

        if line.startswith("## "):
            pdf.ln(4)
            pdf.set_font("Helvetica", "B", 14)
            pdf.set_text_color(20, 60, 120)
            pdf.multi_cell(0, 8, clean_text(line[3:].strip()))
            pdf.ln(2)
            i += 1
            continue

        if line.startswith("### "):
            pdf.ln(2)
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_text_color(40, 40, 40)
            pdf.multi_cell(0, 7, clean_text(line[4:].strip()))
            pdf.ln(1)
            i += 1
            continue

        if line.startswith("```"):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1
            pdf.set_font("Courier", "", 9)
            pdf.set_fill_color(245, 245, 245)
            block = "\n".join(code_lines)
            pdf.multi_cell(0, 5, clean_text(block), fill=True)
            pdf.ln(3)
            continue

        if line.strip().startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            render_table(pdf, parse_table(table_lines))
            continue

        if line.strip() == "---":
            pdf.ln(2)
            i += 1
            continue

        if line.strip().startswith(">"):
            add_wrapped(pdf, line.strip()[1:].strip(), size=10, style="I")
            i += 1
            continue

        if line.strip().startswith("- "):
            add_wrapped(pdf, "  * " + line.strip()[2:], size=10)
            i += 1
            continue

        if line.strip():
            add_wrapped(pdf, line.strip(), size=10)

        i += 1

    pdf.output(str(OUTPUT))
    print(f"PDF generated: {OUTPUT}")


if __name__ == "__main__":
    build_pdf()
