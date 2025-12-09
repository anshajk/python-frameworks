# tools.py
import logging


# The type hints (str) and the return type (dict) are ESSENTIAL.
# The ADK uses them to tell Gemini what this function expects.
def get_weather_report(city: str) -> dict:
    """
    Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city to fetch weather for (e.g., "London").

    Returns:
        dict: A dictionary containing 'status' and 'report' or 'error_message'.
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Fetching weather for: {city}")

    # Mocking the external API call for this tutorial
    # In production, you would use 'requests.get(...)'
    city_normalized = city.lower().strip()

    mock_db = {
        "london": {"status": "success", "report": "Cloudy, 18C, Humidity 82%"},
        "paris": {"status": "success", "report": "Sunny, 25C, UV Index High"},
        "san francisco": {"status": "success", "report": "Foggy, 14C, Wind 15km/h"},
    }

    if city_normalized in mock_db:
        return mock_db[city_normalized]
    else:
        # Return structured errors so the Agent can handle them!
        return {
            "status": "error",
            "error_message": f"Weather data not available for '{city}'. Try a major capital.",
        }


def analyze_sentiment(text: str) -> dict:
    """
    Analyzes the sentiment of a user's reaction.

    Args:
        text (str): The user's input text.

    Returns:
        dict: Sentiment score and label.
    """
    # Simple keyword heuristic for demo purposes
    text_lower = text.lower()
    if any(x in text_lower for x in ["good", "great", "sunny", "nice"]):
        return {"sentiment": "positive", "confidence": 0.9}
    elif any(x in text_lower for x in ["bad", "rain", "cold", "sad"]):
        return {"sentiment": "negative", "confidence": 0.8}
    return {"sentiment": "neutral", "confidence": 0.5}
