import fitz # Because PyMuPDF is imported as fitz
def extract_pdf_text(pdf_path : str):
    doc = fitz.open(pdf_path)
    pages = []
    
    for page_number in range(len(doc)):
        page = doc.load_page(page_number)
        text = page.get_text()
        pages.append({
            "page": page_number + 1,
            "text": text
        })
    return pages


