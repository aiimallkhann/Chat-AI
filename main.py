import ollama

MODEL_NAME = 'llama3'
SYSTEM_PROMPT = 'You are a helpful, private local AI assistant.'



def main():
    messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]
    
    while True:
        user_input = input('You: ')
        if user_input.strip().lower() in ('exit', 'quit'):
            break
        messages.append(
                {
                    'role' : 'user',
                    'content': user_input
                }
            )
        try:
            print('AI: ', end='', flush=True)
            stream = ollama.chat(model=MODEL_NAME, messages=messages, stream=True)
            
            full_response = ''
            for chunk in stream:
                content = chunk['message']['content']
                print(content, end='', flush=True)
                full_response += content
            print('\n')
            messages.append({'role' : 'assistant', 'content' : full_response})
            
        except Exception as e:
            print (f'Error {e}')
            continue

if __name__ == '__main__':
    main()