from zero_shot_init import client


def role_based_prompting_example():
    """Demonstrates role-based (persona) prompting with the Gemini API."""
    prompt = """
    You are an expert travel guide. Answer the following question in a friendly and knowledgeable tone.
    User: I'm visiting Paris for the first time. What are three must-see attractions?
    Travel Guide:
    """
    print("\n--- Role-Based (Persona) Prompting Example ---")
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    print(f"Prompt:\n{prompt}")
    print(f"Response: {response.text}")
