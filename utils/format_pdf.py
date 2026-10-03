from fpdf import FPDF

def format_pdf(document_text, title="LegalEase Document"):
    if not document_text or not document_text.strip():
        raise ValueError("Document content is empty")

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    pdf.set_title(title)
    pdf.set_font("Times", "B", 16)
    pdf.multi_cell(0, 10, title)
    pdf.ln(5)

    pdf.set_font("Times", size=12)
    for line in document_text.splitlines():
        safe_line = line.encode("latin-1", "replace").decode("latin-1")
        pdf.multi_cell(0, 7, safe_line)

    pdf.set_y(-15)
    pdf.set_font("Times", size=9)
    pdf.cell(0, 10, f"Page {pdf.page_no()}", align="C")

    result = pdf.output(dest="S")
    if isinstance(result, str):
        return result.encode("latin-1")
    return bytes(result)
