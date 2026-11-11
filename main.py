import sys
from pathlib import Path
import numpy as np

from read_pdf import read_pdf
from read_docx import read_docx
from read_text import read_text, chunk_text
from embedder import get_embedding
from math_logic import cosine_similarity
from llm import build_prompt, generator
from file_saver import save_text

def load_document(file_path, should_save):
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
        
    return chunk_text(text)

def main():
    print("ChatAI - Local RAG Assistant")
    file_path = input("Enter document path: ").strip()
    save_input = input("Save extracted text to docs/ folder? (y/n): ").strip().lower()
    
    should_save = save_input == 'y'
    
    try:
        chunks = load_document(file_path, should_save)
    except Exception as e:
        print(f"Error loading document: {e}")
        sys.exit(1)
        
    print("Indexing document...")
    chunk_data = []
    for chunk in chunks:
        emb = np.array(get_embedding(chunk))
        chunk_data.append((chunk, emb))
        
    print("Ready.\n")
    
    while True:
        question = input("You: ").strip()
        if question.lower() in ('exit', 'quit'):
            break
        if not question:
            continue
            
        q_emb = np.array(get_embedding(question))
        
        best_chunk = ""
        max_score = -1.0
        
        for chunk, c_emb in chunk_data:
            score = cosine_similarity(q_emb, c_emb)
            if score > max_score:
                max_score = score
                best_chunk = chunk
                
        prompt = build_prompt(question, best_chunk)
        answer = generator(prompt)
        
        print(f"AI: {answer}\n")

if __name__ == '__main__':
    main()