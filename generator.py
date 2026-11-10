import httpx

SYSTEM_PROMPT = 'You are a document assistant. Use strictly the following context to answer the question. If the answer is not in the context, say I cannot answer this based on the document.'

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

def build_prompt(question, context):
    return f'''{SYSTEM_PROMPT}

Context:
{context}

Question:
{question}

'''