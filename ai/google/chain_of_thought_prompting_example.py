from zero_shot_init import client


def chain_of_thought_prompting_example():
    """Demonstrates chain-of-thought prompting with the Gemini API."""
    prompt = """
    Q: Sarah has a budget of $50. She wants to buy a book that costs $15 and a board game that costs $25. Does she have enough money? If so, how much will she have left?
    A: Sarah wants to buy a book for $15 and a board game for $25.
    The total cost of the items is $15 + $25 = $40.
    Her budget is $50.
    Since $40 is less than or equal to $50, she has enough money.
    The money left will be $50 - $40 = $10.

    Q: A baker made 3 batches of cookies. Each batch had 12 cookies. He sold 20 cookies. How many cookies does he have left?
    A:
    """
    print("\n--- Chain-of-Thought Prompting Example ---")
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    print(f"Prompt:\n{prompt}")
    print(f"Response: {response.text}")
