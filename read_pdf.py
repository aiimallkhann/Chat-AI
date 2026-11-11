import os
import re
import shutil
from pathlib import Path
import pymupdf

def find_tessdata():
    env = os.environ.get('TESSDATA_PREFIX')
    if env and Path(env).is_dir():
        return env
    
    exe = shutil.which('tesseract')
    if exe:
        return str(Path(exe).resolve().parent / 'tessdata')
        
    candidates = [
        r'C:\Program Files\Tesseract-OCR\tessdata',
        r'C:\Program Files (x86)\Tesseract-OCR\tessdata',
        '/usr/share/tesseract-ocr/5/tessdata',
        '/usr/share/tessdata'
    ]
    
    for p in candidates:
        if Path(p).is_dir():
            return p
    return None

def clean_text(text):
    text = text.replace('\u00ad', '')
    text = re.sub(r'-\n(\w)', r'\1', text)
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    return re.sub(r'[ \t]+', ' ', text).strip()

def read_pdf(file_path, max_pages=None, lang='eng', dpi=200):
    file_path = Path(file_path)
    if not file_path.is_file():
        raise FileNotFoundError(f'Invalid file path: {file_path}')

    tessdata = find_tessdata()
    if tessdata:
        os.environ['TESSDATA_PREFIX'] = tessdata

    pymupdf.TOOLS.mupdf_display_errors(False)
    pages = []
    
    with pymupdf.open(file_path) as pdf:
        limit = len(pdf) if max_pages is None else min(max_pages, len(pdf))
        
        for i in range(limit):
            page = pdf.load_page(i)
            text = page.get_text()
            
            if len(text.strip()) < 20 and tessdata:
                try:
                    text = page.get_text(textpage=page.get_textpage_ocr(language=lang, dpi=dpi, full=True))
                except Exception:
                    pass
            
            text = clean_text(text)
            if len(text) >= 30:
                pages.append(text)
                
    result = '\n\n'.join(pages).strip()
    if not result:
        raise ValueError(f'No usable text found in {file_path.name}')
    
    return result

def chunk_text(text, size=800, overlap=150):
    step = max(1, size - overlap)
    return [text[i:i + size] for i in range(0, len(text), step) if len(text[i:i + size].strip()) > 30]