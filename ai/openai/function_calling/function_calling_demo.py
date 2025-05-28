import os
import json
from openai import OpenAI
from typing import Dict, Any, List

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


# Example 1: Simple weather function
def get_weather(location: str, unit: str = "celsius") -> Dict[str, Any]:
    """Mock function to get weather data"""
    # In a real application, this would call a weather API
    mock_weather_data = {
        "New York": {"temperature": 22, "condition": "Sunny"},
        "London": {"temperature": 18, "condition": "Cloudy"},
        "Tokyo": {"temperature": 25, "condition": "Partly cloudy"},
    }

    weather = mock_weather_data.get(
        location, {"temperature": 20, "condition": "Unknown"}
    )

    if unit == "fahrenheit":
        weather["temperature"] = weather["temperature"] * 9 / 5 + 32

    return {
        "location": location,
        "temperature": weather["temperature"],
        "unit": unit,
        "condition": weather["condition"],
    }


# Example 2: Calculator functions
def calculate(operation: str, a: float, b: float) -> float:
    """Perform basic arithmetic operations"""
    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else "Error: Division by zero",
    }
    return operations.get(operation, lambda x, y: "Error: Unknown operation")(a, b)


def convert_units(value: float, from_unit: str, to_unit: str) -> Dict[str, Any]:
    """Convert between different units"""
    # Simple conversion factors (to meters as base)
    to_meters = {
        "meters": 1,
        "feet": 0.3048,
        "inches": 0.0254,
        "kilometers": 1000,
        "miles": 1609.34,
    }

    if from_unit not in to_meters or to_unit not in to_meters:
        return {"error": "Unsupported unit"}

    # Convert to meters first, then to target unit
    value_in_meters = value * to_meters[from_unit]
    converted_value = value_in_meters / to_meters[to_unit]

    return {
        "original_value": value,
        "original_unit": from_unit,
        "converted_value": converted_value,
        "converted_unit": to_unit,
    }


# Function schemas for OpenAI
weather_function = {
    "name": "get_weather",
    "description": "Get the current weather in a given location",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city name, e.g. New York, London, Tokyo",
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "The temperature unit",
            },
        },
        "required": ["location"],
    },
}

calculator_function = {
    "name": "calculate",
    "description": "Perform basic arithmetic operations",
    "parameters": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["add", "subtract", "multiply", "divide"],
                "description": "The arithmetic operation to perform",
            },
            "a": {"type": "number", "description": "The first number"},
            "b": {"type": "number", "description": "The second number"},
        },
        "required": ["operation", "a", "b"],
    },
}

converter_function = {
    "name": "convert_units",
    "description": "Convert values between different units of measurement",
    "parameters": {
        "type": "object",
        "properties": {
            "value": {"type": "number", "description": "The value to convert"},
            "from_unit": {
                "type": "string",
                "enum": ["meters", "feet", "inches", "kilometers", "miles"],
                "description": "The unit to convert from",
            },
            "to_unit": {
                "type": "string",
                "enum": ["meters", "feet", "inches", "kilometers", "miles"],
                "description": "The unit to convert to",
            },
        },
        "required": ["value", "from_unit", "to_unit"],
    },
}


def run_conversation(messages: List[Dict[str, str]], functions: List[Dict]) -> str:
    """Run a conversation with function calling"""
    # Available functions mapping
    available_functions = {
        "get_weather": get_weather,
        "calculate": calculate,
        "convert_units": convert_units,
    }

    # Initial API call
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        functions=functions,
        function_call="auto",
    )

    response_message = response.choices[0].message

    # Check if GPT wants to call a function
    if response_message.function_call:
        function_name = response_message.function_call.name
        function_args = json.loads(response_message.function_call.arguments)

        # Call the function
        function_to_call = available_functions[function_name]
        function_response = function_to_call(**function_args)

        # Add function response to messages
        messages.append(response_message.model_dump())
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": json.dumps(function_response),
            }
        )

        # Get final response from GPT
        second_response = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=messages
        )

        return second_response.choices[0].message.content

    return response_message.content


def main():
    print("=== OpenAI Function Calling Examples ===\n")

    # Example 1: Weather lookup
    print("Example 1: Weather Lookup")
    print("-" * 30)

    weather_messages = [
        {"role": "user", "content": "What's the weather like in New York and Tokyo?"}
    ]

    result = run_conversation(weather_messages, [weather_function])
    print(f"User: {weather_messages[0]['content']}")
    print(f"Assistant: {result}\n")

    # Example 2: Calculator and converter
    print("Example 2: Calculator and Unit Converter")
    print("-" * 30)

    calc_messages = [
        {
            "role": "user",
            "content": "What is 25 multiplied by 4? Also, convert 100 feet to meters.",
        }
    ]

    result = run_conversation(calc_messages, [calculator_function, converter_function])
    print(f"User: {calc_messages[0]['content']}")
    print(f"Assistant: {result}\n")

    # Example 3: Complex calculation
    print("Example 3: Complex Request")
    print("-" * 30)

    complex_messages = [
        {
            "role": "user",
            "content": "If I'm traveling 60 miles, how many kilometers is that? And what's 60 divided by 2.5?",
        }
    ]

    result = run_conversation(
        complex_messages, [calculator_function, converter_function]
    )
    print(f"User: {complex_messages[0]['content']}")
    print(f"Assistant: {result}\n")


if __name__ == "__main__":
    main()
