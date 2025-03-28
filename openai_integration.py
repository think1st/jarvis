import openai
from config_manager import load_config

def generate_openai_response(prompt, model="gpt-3.5-turbo"):
    config = load_config()
    api_key = config.get("openai_api_key")

    if not api_key:
        return "[ERROR] Missing OpenAI API key."

    openai.api_key = api_key

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=100,
        )
        return response['choices'][0]['message']['content'].strip()

    except Exception as e:
        print(f"[ERROR] OpenAI request failed: {e}")
        return "[Jarvis dreaming failed gracefully.]"
