from zero_shot_init import client


def few_shot_prompting_example():
    """Demonstrates few-shot prompting with the Gemini API."""
    prompt_parts = [
        "User: What is the capital of France?",
        "Model: Paris.",
        "User: What is the capital of Japan?",
        "Model: Tokyo.",
        "User: What is the capital of Australia?",
        "Model: ",  # The model will complete this
    ]
    contents = "\n".join(prompt_parts)

    print("\n--- Few-Shot Prompting Example ---")
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=contents
    )
    print(f"Prompt:\n{contents}")
    print(f"Response: {response.text}")
