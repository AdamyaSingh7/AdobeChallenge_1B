# core/reader.py
import fitz  # PyMuPDF

def extract_pages(path: str) -> list[str]:
    """
    Read each page’s full text.
    Returns a list of strings, one per page.
    """
    doc = fitz.open(path)
    pages = [page.get_text("text") for page in doc]
    doc.close()
    return pages
