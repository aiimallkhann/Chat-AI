import httpx

def get_embedding (text, model='nomic-embed-text'):
    url = 'http://localhost:11434/api/embeddings'
    payload = {
        'model': model,
        'prompt': text
    }
    
    try:
        with httpx.Client() as client:
            response = client.post(url, json=payload, timeout=30.0)
            response.raise_for_status()
            
            data = response.json()
            
            return data.get('embedding', [])
        
    except httpx.HTTPError as e:
        print(f'Error generating embedding {e}')
        return []