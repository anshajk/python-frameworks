from zero_shot_init import client


def tree_of_thought_prompting_example():
    """Demonstrates tree-of-thought prompting with the Gemini API."""
    prompt = """
    Q: There are three boxes. One contains only apples, one contains only oranges, and one contains both apples and oranges. The boxes are labeled 'apples', 'oranges', and 'apples and oranges', but all labels are wrong. You may pick one fruit from one box. How can you label all the boxes correctly?
    A: Let's consider the possibilities step by step:
    - Since all labels are wrong, the box labeled 'apples and oranges' cannot contain both. It must contain only apples or only oranges.
    - If we pick a fruit from the 'apples and oranges' box and get an apple, then this box must be 'apples'.
    - The box labeled 'oranges' cannot be oranges, so if 'apples and oranges' is 'apples', 'oranges' must be 'both', and 'apples' must be 'oranges'.
    - If we pick an orange from the 'apples and oranges' box, then it must be 'oranges', and the rest follow similarly.
    So, by picking one fruit from the 'apples and oranges' box and relabeling based on what we find, we can correctly label all boxes.

    Q: A farmer has a fox, a chicken, and a bag of grain. He must cross a river with only one item at a time. If left alone, the fox will eat the chicken, and the chicken will eat the grain. How can he get all three across safely?
    A:
    """
    print("\n--- Tree-of-Thought Prompting Example ---")
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    print(f"Prompt:\n{prompt}")
    print(f"Response: {response.text}")
