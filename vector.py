from embedder import get_embedding
import numpy as np

def cosine_similarity(vec1, vec2):
    vec_dot = np.dot(vec1, vec2)

    vec1_norm = np.linalg.norm(vec1)
    vec2_norm = np.linalg.norm(vec2)
    
    vec_norm_prod = vec1_norm * vec2_norm
    
    return (vec_dot) / vec_norm_prod

if __name__ == '__main__':
    text1 = input('Enter first text: ')
    text2 = input('Enter second text: ')
    
    embed_text1 = get_embedding(text1)
    embed_text2 = get_embedding(text2)
    
    np_text1 = np.array(embed_text1)
    np_text2 = np.array(embed_text2)
    
    similarity = cosine_similarity(np_text1, np_text2)
    print(f'Similarity Score: {similarity:.4f}')