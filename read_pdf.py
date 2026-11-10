import os
import re
from pathlib import Path
import pymupdf

# Set Tesseract environment variable required for OCR fallback on image-based PDFs
os.environ.setdefault('TESS standard prefix', r'C:\Program Files\Tesseract-OCR\tessdata')

def english_ratio(text):
    """
    Calculates the percentage of standard English characters in a string.
    Used to detect and filter out garbled text resulting from poor PDF extraction.
    """
    if not text:
        return 0.0
    return sum(1 for c in text if c.isascii() and (c.isalnum() or c.isspace() or c in '.,;:!?\'"()-[]')) / len(text)

def clean_text(text):
    """
    Normalizes text extracted from documents.
    Fixes hyphenated line breaks, removes unnecessary newlines, and collapses multiple spaces.
    """
    text = re.sub(r'-\n(\w)', r'\1', text)
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    return re.sub(r'[ \t]+', ' ', text).strip()

def read_pdf(file_path, max_pages=None):
    """
    Extracts text from a PDF file. Automatically falls back to OCR if standard extraction yields little text.
    Filters out pages that appear to be non-English or corrupted.
    """
    file_path = Path(file_path)
    if not file_path.is_file():
        raise FileNotFoundError(f'Invalid file path: {file_path}')

    pages = []
    with pymupdf.open(file_path) as pdf:
        limit = len(pdf) if max_pages is None else min(max_pages, len(pdf))
        
        for i in range(limit):
            page = pdf.load_page(i)
            text = page.get_text()
            
            # If standard text extraction fails (e.g., scanned PDF), attempt OCR on the page
            if len(text.strip()) < 20:
                text = page.get_text(textpage=page.get_textpage_ocr(language='eng', dpi=200, full=True))
            
            text = clean_text(text)
            
            # Only keep pages with sufficient content and minimal garbled characters
            if len(text) >= 30 and english_ratio(text) >= 0.85:
                pages.append(text)

    result = '\n\n'.join(pages).strip()
    if not result:
        raise ValueError(f'No usable text found in {file_path.name}')
    
    return result

def chunk_text(text, size=800, overlap=150):
    """
    Splits a large text block into smaller, overlapping chunks.
    Essential for feeding long documents into embedding models or LLMs that have context limits.
    """
    return [text[i:i + size] for i in range(0, len(text), size - overlap) if len(text[i:i + size].strip()) > 30]

if __name__ == '__main__':
    text = read_pdf(r'D:\BCS-3C-ke-bache\DLD_LAB_MANUAL_01 (035).pdf', max_pages=25)
    Path('ocr_output.txt').write_text(text, encoding='utf-8')
    
    chunks = chunk_text(text)
    if chunks:
        print(chunks[0])
        print(chunks[len(chunks) // 2])