import httpx

def generator(prompt, model='llama3'):
    url = 'http://localhost:11434/api/generate'
    payload = {
        'model': model,
        'prompt' : prompt,
        'stream' : False
    }
    
    try:
        with httpx.Client() as client:
            response = client.post(url, json=payload, timeout=300.0)
            response.raise_for_status()
            
            data = response.json()
            
            return data.get('response', '')
    except httpx.HTTPError as e:
        print(f'HTTP Error {e}')
        return ''
    