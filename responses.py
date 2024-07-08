import random
import ollama

def get_response(message: str) -> str:
    p_message = message.lower()
    
    if p_message.lower() == "hello":
        return "Hey there!"

    if p_message.lower() == "roll":
        return str(random.randint(1, 6))

    return "I don't understand."


def get_ollama_response(model: str, role: str,message: str) -> str:
    return ollama.chat(
        model=model,
        messages=[{'role': role, 'content': message}],
        stream=False
    )['message']['content']