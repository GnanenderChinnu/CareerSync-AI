from pathlib import Path


def extract_resume_text(uploaded_file):
    suffix = Path(uploaded_file.name).suffix.lower()
    uploaded_file.seek(0)

    if suffix == ".pdf":
        return extract_pdf_text(uploaded_file)
    if suffix == ".docx":
        return extract_docx_text(uploaded_file)
    if suffix == ".txt":
        return uploaded_file.read().decode("utf-8", errors="ignore")

    return ""


def extract_pdf_text(uploaded_file):
    from pypdf import PdfReader

    reader = PdfReader(uploaded_file)
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(page.strip() for page in pages if page.strip())


def extract_docx_text(uploaded_file):
    from docx import Document

    document = Document(uploaded_file)
    paragraphs = [paragraph.text.strip() for paragraph in document.paragraphs if paragraph.text.strip()]
    return "\n".join(paragraphs)
