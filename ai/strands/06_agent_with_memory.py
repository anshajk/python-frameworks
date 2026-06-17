"""
Agent with Memory and Conversation History Example
This example demonstrates how to maintain conversation context and memory in Strands agents.
"""

from strands import Agent, tool
from typing import List, Dict, Any
import json


class ConversationMemory:
    """Simple conversation memory to track user preferences and context."""
    
    def __init__(self):
        self.memory = {}
        self.history = []
    
    def store(self, key: str, value: Any):
        """Store information in memory."""
        self.memory[key] = value
        self.history.append({"action": "store", "key": key, "value": value})
    
    def retrieve(self, key: str) -> Any:
        """Retrieve information from memory."""
        return self.memory.get(key)
    
    def get_all(self) -> dict:
        """Get all stored information."""
        return self.memory.copy()
    
    def get_history(self) -> List[dict]:
        """Get conversation history."""
        return self.history.copy()


# Global memory instance
memory = ConversationMemory()


@tool
def remember_preference(key: str, value: str) -> str:
    """
    Store a user preference or piece of information.
    
    Args:
        key: The key to store the information under
        value: The value to store
        
    Returns:
        Confirmation message
    """
    memory.store(key, value)
    return f"I've remembered that your {key} is {value}"


@tool
def recall_preference(key: str) -> str:
    """
    Recall a previously stored user preference.
    
    Args:
        key: The key to retrieve
        
    Returns:
        The stored value or a message if not found
    """
    value = memory.retrieve(key)
    if value:
        return f"Your {key} is {value}"
    return f"I don't have any information about {key}"


@tool
def list_all_memories() -> str:
    """
    List all stored memories and preferences.
    
    Returns:
        JSON string of all memories
    """
    all_memories = memory.get_all()
    if all_memories:
        return json.dumps(all_memories, indent=2)
    return "No memories stored yet"


@tool
def clear_memory(key: str = None) -> str:
    """
    Clear a specific memory or all memories.
    
    Args:
        key: The key to clear (if None, clears all)
        
    Returns:
        Confirmation message
    """
    if key:
        if key in memory.memory:
            del memory.memory[key]
            return f"Cleared memory for {key}"
        return f"No memory found for {key}"
    else:
        memory.memory.clear()
        return "All memories cleared"


@tool
def add_note(note: str) -> str:
    """
    Add a note to the conversation history.
    
    Args:
        note: The note to add
        
    Returns:
        Confirmation message
    """
    memory.history.append({"action": "note", "content": note})
    return f"Note added: {note}"


def main():
    """
    Create an agent with memory capabilities.
    """
    print("=== Agent with Memory and Conversation History Example ===\n")
    
    # Create an agent with memory tools
    agent = Agent(tools=[
        remember_preference,
        recall_preference,
        list_all_memories,
        clear_memory,
        add_note
    ])
    
    # Conversation demonstrating memory usage
    conversation = [
        "Remember that my favorite color is blue",
        "Remember that my name is Alice",
        "What's my favorite color?",
        "What's my name?",
        "Show me all the things you remember about me",
        "Add a note that I prefer morning meetings",
        "Clear my favorite color from memory",
        "What's my favorite color now?"
    ]
    
    for query in conversation:
        print(f"User: {query}")
        response = agent(query)
        print(f"Agent: {response}\n")
        print("-" * 80 + "\n")
    
    # Show conversation history
    print("=== Conversation History ===")
    print(json.dumps(memory.get_history(), indent=2))


if __name__ == "__main__":
    main()
