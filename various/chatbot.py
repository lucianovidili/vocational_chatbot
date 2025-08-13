import ollama

def main():
    print("Welcome to your local chatbot! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break

        response = ollama.chat(model='mistral', messages=[
            {'role': 'user', 'content': user_input}
        ])

        print("Bot:", response['message']['content'])

if __name__ == "__main__":
    main()