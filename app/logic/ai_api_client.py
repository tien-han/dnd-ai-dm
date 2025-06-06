import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

model = "deepseek/deepseek-r1-0528-qwen3-8b:free"
PROMPT = "You are a creative Dungeon Master for a fantasy RPG." #temp prompt for testing connection

def get_ai_response(user_input: str):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": user_input}
        ]
    }
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as error:
        print(response.text)


        return f"AI request failed: {error}"

if __name__ == "__main__":    #temp function to test connection
    user_input = "Describe a mysterious forest."
    print("AI Response:", get_ai_response(user_input))