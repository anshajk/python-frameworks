"""
Agent with Calculator Tool Example
This example demonstrates using calculator tools for mathematical operations.
"""

from strands import Agent, tool


@tool
def add(a: float, b: float) -> float:
    """
    Add two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        The sum of a and b
    """
    return a + b


@tool
def subtract(a: float, b: float) -> float:
    """
    Subtract b from a.
    
    Args:
        a: Number to subtract from
        b: Number to subtract
        
    Returns:
        The difference of a and b
    """
    return a - b


@tool
def multiply(a: float, b: float) -> float:
    """
    Multiply two numbers.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        The product of a and b
    """
    return a * b


@tool
def divide(a: float, b: float) -> float:
    """
    Divide a by b.
    
    Args:
        a: Numerator
        b: Denominator
        
    Returns:
        The quotient of a and b
        
    Raises:
        ValueError: If b is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


@tool
def power(base: float, exponent: float) -> float:
    """
    Raise base to the power of exponent.
    
    Args:
        base: The base number
        exponent: The exponent
        
    Returns:
        base raised to the power of exponent
    """
    return base ** exponent


def main():
    """
    Create an agent with calculator tools to solve math problems.
    """
    print("=== Agent with Calculator Tools Example ===\n")
    
    # Create an agent with math tools
    agent = Agent(tools=[add, subtract, multiply, divide, power])
    
    # Math problems
    problems = [
        "What is 15 plus 27?",
        "Calculate 144 divided by 12",
        "What is 2 to the power of 10?",
        "If I have 100 dollars and spend 35.50, then earn 20.75, how much do I have?",
        "Calculate the area of a rectangle with length 12.5 and width 8.3"
    ]
    
    for problem in problems:
        print(f"Problem: {problem}")
        response = agent(problem)
        print(f"Agent: {response}\n")
        print("-" * 80 + "\n")


if __name__ == "__main__":
    main()
