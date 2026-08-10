from pathlib import Path

from pypdf import PdfReader
from docx import Document


def extract_from_txt(file_path):
    """
    Extract text from a TXT file.
    """

    with open(
        file_path,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as file:

        return file.read()


def extract_from_pdf(file_path):
    """
    Extract text from a PDF file.
    """

    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:

        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


def extract_from_docx(file_path):
    """
    Extract text from a DOCX file.
    """

    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:

        if paragraph.text.strip():

            paragraphs.append(
                paragraph.text
            )

    return "\n".join(paragraphs)


def extract_resume_text(file_path):
    """
    Extract resume text based on file type.

    Supported formats:
    TXT, PDF, DOCX
    """

    file_path = Path(file_path)

    extension = file_path.suffix.lower()

    if extension == ".txt":

        return extract_from_txt(file_path)

    elif extension == ".pdf":

        return extract_from_pdf(file_path)

    elif extension == ".docx":

        return extract_from_docx(file_path)

    else:

        raise ValueError(
            f"Unsupported file type: {extension}"
        )