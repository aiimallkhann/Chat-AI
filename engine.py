from pathlib import Path
import numpy as np

from read_pdf import read_pdf
from read_docx import read_docx
from read_txt import read_text, chunk_text
from embedder import get_embedding
from vector import cosine_similarity
from generator import build_prompt, generator
from saveFile import save_text

_chunk_data = []

def load_document(file_path, should_save):
    global _chunk_data
    _chunk_data.clear()
    
    path = Path(file_path)
    ext = path.suffix.lower()
    
    if ext == '.pdf':
        text = read_pdf(file_path)
    elif ext == '.docx':
        text = read_docx(file_path)
    elif ext == '.txt':
        text = read_text(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")
        
    if should_save:
        save_text(file_path, text)
        
    chunks = chunk_text(text)
    for chunk in chunks:
        emb = np.array(get_embedding(chunk))
        _chunk_data.append((chunk, emb))

def get_answer(question):
    if not _chunk_data:
        return "Please load a document first."
        
    q_emb = np.array(get_embedding(question))
    
    best_chunk = ""
    max_score = -1.0
    
    for chunk, c_emb in _chunk_data:
        score = cosine_similarity(q_emb, c_emb)
        if score > max_score:
            max_score = score
            best_chunk = chunk
            
    prompt = build_prompt(question, best_chunk)
    return generator(prompt)