from google import genai
import os
from zero_shot_prompting_example import zero_shot_prompting_example
from few_shot_prompting_example import few_shot_prompting_example
from chain_of_thought_prompting_example import chain_of_thought_prompting_example
from tree_of_thought_prompting_example import tree_of_thought_prompting_example
from interview_pattern_prompting_example import interview_pattern_prompting_example
from role_based_prompting_example import role_based_prompting_example

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

client = genai.Client(api_key=gemini_api_key)

response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain how AI works in three sentences"
)
print(response.text)

if __name__ == "__main__":
    zero_shot_prompting_example()
    few_shot_prompting_example()
    chain_of_thought_prompting_example()
    tree_of_thought_prompting_example()
    interview_pattern_prompting_example()
    role_based_prompting_example()
