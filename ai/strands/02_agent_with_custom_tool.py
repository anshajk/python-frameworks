"""
Agent with Custom Tool Example
This example shows how to create custom tools and integrate them with a Strands agent.
"""

from strands import Agent, tool


@tool
def word_count(text: str) -> int:
    """
    Count the number of words in the provided text.
    
    Args:
        text: The text to count words in
        
    Returns:
        The number of words in the text
    """
    return len(text.split())


@tool
def reverse_text(text: str) -> str:
    """
    Reverse the order of characters in the provided text.
    
    Args:
        text: The text to reverse
        
    Returns:
        The reversed text
    """
    return text[::-1]


@tool
def text_stats(text: str) -> dict:
    """
    Get various statistics about the provided text.
    
    Args:
        text: The text to analyze
        
    Returns:
        A dictionary with text statistics
    """
    words = text.split()
    return {
        "character_count": len(text),
        "word_count": len(words),
        "sentence_count": text.count('.') + text.count('!') + text.count('?'),
        "average_word_length": sum(len(word) for word in words) / len(words) if words else 0
    }


def main():
    """
    Create an agent with custom text processing tools.
    """
    print("=== Agent with Custom Tools Example ===\n")
    
    # Create an agent with custom tools
    agent = Agent(tools=[word_count, reverse_text, text_stats])
    
    # Test queries that use different tools
    queries = [
        "How many words are in this sentence: 'The quick brown fox jumps over the lazy dog'?",
        "Can you reverse this text: 'Hello World'?",
        "Give me statistics about this text: 'Python is an amazing programming language. It is widely used in AI and data science!'"
    ]
    
    for query in queries:
        print(f"Query: {query}")
        response = agent(query)
        print(f"Agent: {response}\n")
        print("-" * 80 + "\n")


if __name__ == "__main__":
    main()
