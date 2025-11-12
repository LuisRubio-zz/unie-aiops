import os
from dotenv import load_dotenv
from google import genai

def main():
    # Load environment variables
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not found in environment.")

    # Create client
    client = genai.Client(api_key=api_key)

    model_name = "gemini-2.5-flash"

    print("🤖 Gemini Chat (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("👋 Goodbye!")
            break

        try:
            response = client.models.generate_content(
                model=model_name,
                contents=user_input,
            )
            print(f"Gemini: {response.text}\n")
        except Exception as e:
            print(f"⚠️ Error: {e}\n")

if __name__ == "__main__":
    main()
