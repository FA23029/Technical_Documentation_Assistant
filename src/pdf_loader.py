import fitz
from pathlib import Path


def load_pdf(file_path):
    document = fitz.open(file_path)

    pages = []

    for page_number, page in enumerate(document):
        text = page.get_text()

        if text.strip():
            pages.append({
                "text": text,
                "source": Path(file_path).name,
                "page": page_number + 1
            })

    document.close()

    return pages


def load_all_pdfs(folder_path):
    folder = Path(folder_path)

    all_pages = []

    for pdf_file in folder.glob("*.pdf"):
        pages = load_pdf(pdf_file)
        all_pages.extend(pages)

    return all_pages