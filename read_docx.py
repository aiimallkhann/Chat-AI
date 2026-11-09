import re
from pathlib import Path
import docx

def clean_text(text):
    text = re.sub(r'-\n(\w)', r'\1', text)
    text = re.sub(r'(?<!\n)\n (?!\n)', ' ', text)
    return re.sub(r'[ \t]+', ' ', text)

def chunk_text(text, size=800 ,overlap=150):
    return [text[i:i + size] for i in range(0, len(text), size - overlap) if len(text[i:i + size].strip()) > 30]

def read_docx(file_path, max_pages=None):
    file_path = Path(file_path)
    if not file_path.is_file():
        raise FileNotFoundError(f'Invalid File Path {file_path}')
    doc = docx.Document(file_path)
    
    content = []
    
    for p in doc.paragraph:
        cleaned_text = clean_text(p.text)
        if cleaned_text is not None:
            return content.append(cleaned_text)
        for tables in doc.tables:
            for rows in tables.rows:
                
        