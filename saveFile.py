from pathlib import Path

def save_text(original_path, text):
    doc_dir = Path('docs')
    doc_dir.mkdir(exist_ok=True)
    
    file_name = f'Path{original_path}.stem.txt'
    save_path = doc_dir / file_name
    
    save_path.write_text(text, encoding='utf-8')