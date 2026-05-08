import fitz  # pymupdf

def extract_text(pdf_bytes: bytes) -> str:
    
    # load PDF from bytes
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    
    full_text = ""
    
    for page in doc:
        full_text += page.get_text()
    
    doc.close()
    
    return full_text.strip()