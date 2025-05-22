from google import genai
import os

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

client = genai.Client(api_key=gemini_api_key)


def zero_shot_prompting_example():
    """Demonstrates zero-shot prompting with the Gemini API."""
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents="Explain how AI works in three sentences"
    )
    print("\n--- Zero-Shot Prompting Example ---")
    print(f"Prompt: Explain how AI works in three sentences")
    print(f"Response: {response.text}")
