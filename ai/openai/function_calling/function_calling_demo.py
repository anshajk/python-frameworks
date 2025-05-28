from openai import OpenAI
import os
import json
from typing import Dict, Any, List
import time

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Example 1


def get_weather(location: str, unit: str = "celsius") -> Dict[str, Any]:
    """Mock function to get weather data"""
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


def calculate(operation: str, a: float, b: float) -> float:
    """Performs basic artihmetic operations"""
    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: (
            x / y if y != 0 else "Error: Divizion by zero isn't allowed"
        ),
    }
    return operations.get(operation, lambda x, y: "Error Unknown Operation")(a, b)


def convert_units(value: float, from_unit: str, to_unit: str) -> Dict[str, Any]:
    """Convert between different units"""
    to_meters = {
        "meters": 1,
        "feet": 0.3048,
        "inches": 0.0254,
        "kilometers": 1000,
        "miles": 1609.34,
    }
    if from_unit not in to_meters or to_unit not in to_meters:
        return {"error": "Unsupported unit"}

    value_in_meters = value * to_meters[from_unit]
    converted_value = value_in_meters / to_meters[to_unit]

    return {
        "original_value": value,
        "original_unit": from_unit,
        "converted_value": converted_value,
        "converted_unit": to_unit,
    }


# Function schema for OpenAI

weather_function = {
    "type": "function",
    "name": "get_weather",
    "description": "Get the weather in a given location",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city name like New York, London, Tokyo",
            },
            "unit": {
                "type": "string",
                "emum": ["celsius", "fahrenheit"],
                "description": "The temperature unit",
            },
        },
        "required": ["location", "unit"],
        "additionalProperties": False,
    },
    "strict": True,
}

calculator_function = {
    "type": "function",
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
        "additionalProperties": False,
    },
    "strict": True,
}

converter_function = {
    "type": "function",
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
        "additionalProperties": False,
    },
    "strict": True,
}


def run_conversation(messages: List[Dict[str, str]], functions: List[Dict]) -> str:
    """Run a conversation with function calling"""
    available_functions = {
        "get_weather": get_weather,
        "calculate": calculate,
        "convert_units": convert_units,
    }

    # API Call
    response = client.responses.create(
        model="gpt-4.1", input=messages, tools=functions, tool_choice="auto"
    )

    tool_call = response.output[0]

    while tool_call.type == "function_call":
        function_name = tool_call.name
        function_args = json.loads(tool_call.arguments)

        function_to_call = available_functions[function_name]
        function_response = function_to_call(**function_args)

        messages.append(tool_call)

        messages.append(
            {
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": json.dumps(function_response),
            }
        )

        response = client.responses.create(
            model="gpt-4.1", input=messages, tools=functions
        )

        tool_call = response.output[0]

    return response.output_text


def main():
    print("-- OpenAI Function calling example -- ")

    message = [
        {
            "role": "user",
            "content": "If I'm travelling 60 miles, how many kilometers is that? And what's 60 divided by 2.5? And, what's the weather like in London?",
        }
    ]

    result = run_conversation(
        message, [calculator_function, converter_function, weather_function]
    )

    print(f"User: {message[0]['content']}")
    print(f"Assistant: {result}")


main()
