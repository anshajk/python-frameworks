"""
Agent with AWS Bedrock Integration Example
This example demonstrates how to use Strands with AWS Bedrock models.
"""

from strands import Agent, tool
from typing import Dict, Optional
import os


@tool
def analyze_text(text: str) -> Dict[str, any]:
    """
    Analyze text and extract key information.
    
    Args:
        text: The text to analyze
        
    Returns:
        Analysis results including word count, sentence count, etc.
    """
    sentences = text.count('.') + text.count('!') + text.count('?')
    words = len(text.split())
    characters = len(text)
    
    return {
        "word_count": words,
        "sentence_count": sentences,
        "character_count": characters,
        "average_word_length": characters / words if words > 0 else 0
    }


@tool
def classify_text(text: str) -> str:
    """
    Classify text into categories (mock implementation).
    
    Args:
        text: The text to classify
        
    Returns:
        Classification result
    """
    # Simple keyword-based classification
    text_lower = text.lower()
    
    if any(word in text_lower for word in ["technology", "ai", "software", "computer"]):
        return "Technology"
    elif any(word in text_lower for word in ["health", "medical", "doctor", "medicine"]):
        return "Healthcare"
    elif any(word in text_lower for word in ["money", "finance", "investment", "bank"]):
        return "Finance"
    elif any(word in text_lower for word in ["sport", "game", "team", "player"]):
        return "Sports"
    else:
        return "General"


@tool
def extract_entities(text: str) -> Dict[str, list]:
    """
    Extract named entities from text (mock implementation).
    
    Args:
        text: The text to process
        
    Returns:
        Dictionary with entity types and values
    """
    # Mock entity extraction
    words = text.split()
    entities = {
        "organizations": [],
        "locations": [],
        "technologies": []
    }
    
    # Simple pattern matching (in real implementation, use NER model)
    tech_keywords = ["AI", "AWS", "Python", "Bedrock", "Claude", "GPT"]
    org_keywords = ["Amazon", "Google", "Microsoft", "Apple"]
    loc_keywords = ["USA", "Europe", "Asia", "America"]
    
    for word in words:
        if word in tech_keywords:
            entities["technologies"].append(word)
        elif word in org_keywords:
            entities["organizations"].append(word)
        elif word in loc_keywords:
            entities["locations"].append(word)
    
    return entities


def create_bedrock_agent(model_id: str = "anthropic.claude-v2") -> Agent:
    """
    Create an agent configured to use AWS Bedrock.
    
    Args:
        model_id: The Bedrock model ID to use
        
    Returns:
        Configured Agent instance
    """
    # Note: In a real implementation, you would configure the agent with Bedrock
    # For this example, we're showing the structure
    
    print(f"Creating agent with AWS Bedrock model: {model_id}")
    print("Note: Ensure AWS credentials are configured and Bedrock access is enabled")
    
    # Create agent with tools
    agent = Agent(
        tools=[analyze_text, classify_text, extract_entities],
        # In real implementation, you would pass model configuration:
        # model={"provider": "bedrock", "model_id": model_id}
    )
    
    return agent


def main():
    """
    Demonstrate using Strands with AWS Bedrock.
    """
    print("=== Agent with AWS Bedrock Integration Example ===\n")
    
    # Check for AWS configuration
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    print(f"AWS Region: {aws_region}")
    print("Note: This example shows the structure for Bedrock integration.")
    print("Ensure you have AWS credentials configured and Bedrock access enabled.\n")
    
    # Available Bedrock models
    bedrock_models = {
        "claude-v2": "anthropic.claude-v2",
        "claude-instant": "anthropic.claude-instant-v1",
        "titan": "amazon.titan-text-express-v1",
        "llama2": "meta.llama2-70b-chat-v1"
    }
    
    print("Available Bedrock Models:")
    for name, model_id in bedrock_models.items():
        print(f"  - {name}: {model_id}")
    print()
    
    # Create agent with Bedrock
    agent = create_bedrock_agent(bedrock_models["claude-v2"])
    
    # Example queries
    queries = [
        "Analyze this text: 'AWS Bedrock provides access to foundation models from leading AI companies including Anthropic, Meta, and Amazon.'",
        "What category does this belong to: 'The new AI technology is revolutionizing software development'?",
        "Extract entities from: 'Amazon Web Services launched Bedrock in the USA to provide AI capabilities to developers.'"
    ]
    
    for query in queries:
        print(f"Query: {query}")
        response = agent(query)
        print(f"Agent: {response}\n")
        print("-" * 80 + "\n")
    
    # Show configuration info
    print("\n=== Bedrock Configuration Tips ===")
    print("1. Install AWS SDK: pip install boto3")
    print("2. Configure AWS credentials: aws configure")
    print("3. Enable Bedrock model access in AWS Console")
    print("4. Set AWS_REGION environment variable")
    print("5. Ensure IAM permissions for bedrock:InvokeModel")


if __name__ == "__main__":
    main()
