import httpx

def get_embedding(text, model='nomic-embed-text'):
    """
    Fetches a text embedding vector from a local Ollama server.

    Args:
        text (str): The input text to be embedded.
        model (str): The specific embedding model to use. Defaults to 'nomic-embed-text'.

    Returns:
        list: The embedding vector as a list of floats. Returns an empty list [] if the HTTP request fails.
    """
    url = 'http://localhost:11434/api/embeddings'
    payload = {
        'model': model,
        'prompt': text
    }
    
    try:
        # Client context manager enables connection pooling, reducing latency for batch requests
        with httpx.Client() as client:
            # 30-second timeout accounts for the local server's "cold start" model loading time
            response = client.post(url, json=payload, timeout=30.0)
            response.raise_for_status()
            
            data = response.json()
            
            # .get() prevents fatal KeyErrors if the API response is malformed, ensuring batch jobs don't crash
            return data.get('embedding', [])
        
    except httpx.HTTPError as e:
        print(f'Error generating embedding: {e}')
        return []