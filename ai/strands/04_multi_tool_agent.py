"""
Multi-Tool Agent Example
This example demonstrates an agent with multiple tools working together.
"""

from strands import Agent, tool
import random
from datetime import datetime


@tool
def get_weather(location: str) -> dict:
    """
    Get the current weather for a location.
    Note: This is a mock implementation for demonstration purposes.
    
    Args:
        location: The city or location name
        
    Returns:
        A dictionary with weather information
    """
    # Mock weather data
    conditions = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy", "Stormy"]
    temperatures = {
        "New York": 22,
        "London": 15,
        "Tokyo": 25,
        "Paris": 18,
        "Sydney": 28
    }
    
    temp = temperatures.get(location, random.randint(10, 30))
    condition = random.choice(conditions)
    
    return {
        "location": location,
        "temperature": temp,
        "condition": condition,
        "humidity": random.randint(30, 80),
        "wind_speed": random.randint(5, 25)
    }


@tool
def calculate(operation: str, a: float, b: float) -> float:
    """
    Perform a mathematical calculation.
    
    Args:
        operation: The operation to perform (add, subtract, multiply, divide)
        a: First number
        b: Second number
        
    Returns:
        The result of the calculation
    """
    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else "Error: Division by zero"
    }
    return operations.get(operation, lambda x, y: "Error: Unknown operation")(a, b)


@tool
def get_current_time(timezone: str = "UTC") -> str:
    """
    Get the current time.
    
    Args:
        timezone: The timezone (default: UTC)
        
    Returns:
        The current time as a string
    """
    now = datetime.now()
    return f"Current time in {timezone}: {now.strftime('%Y-%m-%d %H:%M:%S')}"


@tool
def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert temperature between Celsius and Fahrenheit.
    
    Args:
        value: The temperature value
        from_unit: The source unit (celsius or fahrenheit)
        to_unit: The target unit (celsius or fahrenheit)
        
    Returns:
        The converted temperature
    """
    if from_unit.lower() == "celsius" and to_unit.lower() == "fahrenheit":
        return (value * 9/5) + 32
    elif from_unit.lower() == "fahrenheit" and to_unit.lower() == "celsius":
        return (value - 32) * 5/9
    else:
        return value


def main():
    """
    Create an agent with multiple tools for different tasks.
    """
    print("=== Multi-Tool Agent Example ===\n")
    
    # Create an agent with multiple tools
    agent = Agent(tools=[get_weather, calculate, get_current_time, convert_temperature])
    
    # Complex queries that may use multiple tools
    queries = [
        "What's the weather like in Tokyo?",
        "What's the current time?",
        "If the temperature in London is 15 Celsius, what is that in Fahrenheit?",
        "What's the weather in New York and if I multiply the temperature by 2, what do I get?",
        "Get the weather for Paris and tell me the time"
    ]
    
    for query in queries:
        print(f"Query: {query}")
        response = agent(query)
        print(f"Agent: {response}\n")
        print("-" * 80 + "\n")


if __name__ == "__main__":
    main()
