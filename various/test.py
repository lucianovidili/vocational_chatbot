import ollama

response = ollama.chat(model='phi3', messages=[
    {'role': 'user', 'content': 'Write me a short poem about the ocean'}
])
print(response['message']['content'])