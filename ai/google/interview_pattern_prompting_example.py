from zero_shot_init import client


def interview_pattern_prompting_example():
    """Demonstrates interview pattern prompting with the Gemini API."""
    prompt = """
    Interviewer: Can you tell me about a time you solved a difficult problem?
    Candidate: Certainly. In my previous job, I encountered a major bug in our production system. I systematically analyzed logs, isolated the root cause, and implemented a fix that prevented future occurrences.
    Interviewer: How do you approach learning a new technology?
    Candidate: I start by reading the official documentation, then build small projects to get hands-on experience, and finally seek feedback from peers or online communities.
    Interviewer: What motivates you in your work?
    Candidate:
    """
    print("\n--- Interview Pattern Prompting Example ---")
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    print(f"Prompt:\n{prompt}")
    print(f"Response: {response.text}")
