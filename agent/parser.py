from pathlib import Path

from pypdf import PdfReader
from docx import Document


def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""

    reader = PdfReader(file_path)

    text = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text.append(page_text)

    return "\n".join(text)


def extract_text_from_docx(file_path):
    """Extract text from a DOCX file."""

    document = Document(file_path)

    text = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text.append(paragraph.text)

    return "\n".join(text)


def extract_text_from_txt(file_path):
    """Extract text from a TXT file."""

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def extract_resume_text(file_path):
    """Extract text from PDF, DOCX, or TXT resume."""

    path = Path(file_path)

    extension = path.suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    elif extension == ".docx":
        return extract_text_from_docx(file_path)

    elif extension == ".txt":
        return extract_text_from_txt(file_path)

    else:
        raise ValueError(
            f"Unsupported file format: {extension}"
        )