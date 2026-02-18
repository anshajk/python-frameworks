"""
Basic Strands Agent Example
This example demonstrates the simplest possible Strands agent with basic text interaction.
"""

from strands import Agent


def main():
    """
    Create and run a basic agent with no tools.
    This agent uses the default LLM to respond to user queries.
    """
    print("=== Basic Strands Agent Example ===\n")
    
    # Create a basic agent with default settings
    agent = Agent()
    
    # Simple conversation
    questions = [
        "What is the capital of France?",
        "Explain quantum computing in simple terms.",
        "What are the benefits of using AI agents?"
    ]
    
    for question in questions:
        print(f"Question: {question}")
        response = agent(question)
        print(f"Agent: {response}\n")
        print("-" * 80 + "\n")


if __name__ == "__main__":
    main()
