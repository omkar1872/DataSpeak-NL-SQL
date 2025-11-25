from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file

def main():
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "Hello from Groq!"}]
        )

        print("✔ Groq API key is working!")
        print(response.choices[0].message.content)

    except Exception as e:
        print("❌ Groq API Failed:", e)

if __name__ == "__main__":
    main()
