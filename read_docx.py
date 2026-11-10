import re
from pathlib import Path
import docx

def clean_text(text):
    """
    Normalizes text extracted from documents.
    Fixes hyphenated line breaks, removes unnecessary newlines, and collapses multiple spaces.
    """
    text = re.sub(r'-\n(\w)', r'\1', text)
    text = re.sub(r'(?<!\n)\n (?!\n)', ' ', text)
    return re.sub(r'[ \t]+', ' ', text)

def chunk_text(text, size=800, overlap=150):
    """
    Splits a large text block into smaller, overlapping chunks.
    Essential for feeding long documents into embedding models or LLMs that have context limits.
    """
    return [text[i:i + size] for i in range(0, len(text), size - overlap) if len(text[i:i + size].strip()) > 30]

def read_docx(file_path, max_pages=None):
    """
    Extracts text from paragraphs and tables in a .docx file.
    """
    file_path = Path(file_path)
    if not file_path.is_file():
        raise FileNotFoundError(f'Invalid File Path {file_path}')
    doc = docx.Document(file_path)
    
    content = []
    
    for p in doc.paragraphs:
        cleaned_text = clean_text(p.text)
        if cleaned_text:
            content.append(cleaned_text)
            
    for t in doc.tables:
        for r in t.rows:
            # Only include cells that actually contain text to avoid empty table rows
            row_data = [clean_text(cell.text) for cell in r.cells if cell.text.strip()]
            if row_data:
                joined_row = ' | '.join(row_data)
                content.append(joined_row)
                
    return '\n\n'.join(content).strip()

if __name__ == '__main__':
    text = read_docx(r'D:\Studies\Software\SOFTWARE NOTES.docx')
    Path('docx_output.txt').write_text(text, encoding='utf-8')
    
    chunks = chunk_text(text)
    if chunks:
        print(chunks[0])
        print(chunks[len(chunks) // 2])