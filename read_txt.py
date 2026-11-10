import re
from pathlib import Path
def clean_text(text):
    text = re.sub(r'-\n(\w)', r'\1', text)
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    return re.sub(r'[ \t]+', ' ', text).strip()


def chunk_text(text, size=800, overlap=150):
    return [text[i:i + size] for i in range(0, len(text), size - overlap) if len(text[i:i + size].strip()) > 30]

def read_text(file_path):
    file_path = Path(file_path)
    if not file_path.is_file():
        raise FileNotFoundError(f'Incorrect file path {file_path}')
    text = file_path.read_text(encoding='utf-8')
    result = clean_text(text)
    
    if not result:
        raise ValueError(f'No usable text found in {file_path.name}')
    return result

if __name__ == '__main__':
    text = read_text(r'D:\Fiverr\Chat-AI\docx_output.txt')
    Path('txt_output.txt').write_text(text, encoding='utf-8')
    
    chunks = chunk_text(text)
    if chunks:
        print(chunks[0])
        print(chunks[len(chunks) // 2])