"""
Production-Ready Agent Example
This example demonstrates a production-ready agent with error handling,
logging, rate limiting, and monitoring capabilities.
"""

from strands import Agent, tool
from typing import Dict, Optional, Any
import logging
import time
import json
from functools import wraps
from datetime import datetime


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RateLimiter:
    """Simple rate limiter for API calls."""
    
    def __init__(self, calls_per_minute: int = 60):
        self.calls_per_minute = calls_per_minute
        self.calls = []
    
    def allow_request(self) -> bool:
        """Check if a request is allowed based on rate limit."""
        now = time.time()
        # Remove calls older than 1 minute
        self.calls = [call_time for call_time in self.calls if now - call_time < 60]
        
        if len(self.calls) < self.calls_per_minute:
            self.calls.append(now)
            return True
        return False


class MetricsCollector:
    """Collect metrics about agent operations."""
    
    def __init__(self):
        self.metrics = {
            "total_calls": 0,
            "successful_calls": 0,
            "failed_calls": 0,
            "total_execution_time": 0.0,
            "tool_usage": {}
        }
    
    def record_call(self, tool_name: str, success: bool, execution_time: float):
        """Record a tool call metric."""
        self.metrics["total_calls"] += 1
        if success:
            self.metrics["successful_calls"] += 1
        else:
            self.metrics["failed_calls"] += 1
        
        self.metrics["total_execution_time"] += execution_time
        
        if tool_name not in self.metrics["tool_usage"]:
            self.metrics["tool_usage"][tool_name] = {"calls": 0, "failures": 0}
        
        self.metrics["tool_usage"][tool_name]["calls"] += 1
        if not success:
            self.metrics["tool_usage"][tool_name]["failures"] += 1
    
    def get_metrics(self) -> Dict:
        """Get collected metrics."""
        return self.metrics.copy()
    
    def reset(self):
        """Reset all metrics."""
        self.__init__()


# Global instances
rate_limiter = RateLimiter(calls_per_minute=30)
metrics = MetricsCollector()


def monitored_tool(func):
    """Decorator to add monitoring to tools."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        tool_name = func.__name__
        
        try:
            # Check rate limit
            if not rate_limiter.allow_request():
                logger.warning(f"Rate limit exceeded for {tool_name}")
                raise Exception("Rate limit exceeded. Please try again later.")
            
            logger.info(f"Executing tool: {tool_name}")
            result = func(*args, **kwargs)
            
            execution_time = time.time() - start_time
            metrics.record_call(tool_name, True, execution_time)
            
            logger.info(f"Tool {tool_name} completed in {execution_time:.3f}s")
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            metrics.record_call(tool_name, False, execution_time)
            
            logger.error(f"Tool {tool_name} failed after {execution_time:.3f}s: {str(e)}")
            raise
    
    return wrapper


@tool
@monitored_tool
def safe_divide(a: float, b: float) -> float:
    """
    Safely divide two numbers with error handling.
    
    Args:
        a: Numerator
        b: Denominator
        
    Returns:
        Result of division
        
    Raises:
        ValueError: If denominator is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


@tool
@monitored_tool
def fetch_data(source: str) -> Dict[str, Any]:
    """
    Fetch data from a source with retry logic.
    
    Args:
        source: The data source identifier
        
    Returns:
        The fetched data
    """
    # Simulate network call with potential failure
    import random
    
    if random.random() < 0.1:  # 10% failure rate for demo
        raise Exception(f"Failed to fetch data from {source}")
    
    # Mock data
    data = {
        "api": {"status": "success", "data": [1, 2, 3, 4, 5]},
        "database": {"status": "success", "records": 100},
        "file": {"status": "success", "content": "Sample file content"}
    }
    
    return data.get(source, {"status": "error", "message": "Unknown source"})


@tool
@monitored_tool
def process_data(data: str, operation: str = "uppercase") -> str:
    """
    Process data with the specified operation.
    
    Args:
        data: The data to process
        operation: The operation to perform
        
    Returns:
        Processed data
    """
    operations = {
        "uppercase": lambda x: x.upper(),
        "lowercase": lambda x: x.lower(),
        "reverse": lambda x: x[::-1],
        "length": lambda x: f"Length: {len(x)}"
    }
    
    if operation not in operations:
        raise ValueError(f"Unknown operation: {operation}")
    
    return operations[operation](data)


@tool
@monitored_tool
def get_system_status() -> Dict[str, Any]:
    """
    Get system status and health metrics.
    
    Returns:
        System status information
    """
    return {
        "timestamp": datetime.now().isoformat(),
        "status": "healthy",
        "uptime": "24h 15m",
        "cpu_usage": "45%",
        "memory_usage": "60%",
        "active_connections": 15
    }


def create_production_agent() -> Agent:
    """
    Create a production-ready agent with all safety features.
    
    Returns:
        Configured Agent instance
    """
    logger.info("Initializing production agent")
    
    agent = Agent(
        tools=[safe_divide, fetch_data, process_data, get_system_status],
        # In production, you'd add more configuration:
        # - Model selection
        # - Timeout settings
        # - Retry logic
        # - Authentication
    )
    
    return agent


def main():
    """
    Demonstrate production-ready agent with monitoring.
    """
    print("=== Production-Ready Agent Example ===\n")
    
    # Create the agent
    agent = create_production_agent()
    
    # Test queries
    queries = [
        "What is 100 divided by 5?",
        "Fetch data from the api source",
        "Process 'Hello World' with uppercase operation",
        "What's the system status?",
        "Try to divide 10 by 0"  # This will fail gracefully
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        try:
            response = agent(query)
            print(f"Agent: {response}")
        except Exception as e:
            print(f"Error: {str(e)}")
        print("-" * 80)
    
    # Display metrics
    print("\n=== Performance Metrics ===")
    print(json.dumps(metrics.get_metrics(), indent=2))
    
    # Production best practices
    print("\n=== Production Best Practices ===")
    print("1. Implement proper error handling and retries")
    print("2. Add rate limiting to prevent abuse")
    print("3. Monitor and log all operations")
    print("4. Collect metrics for performance analysis")
    print("5. Use circuit breakers for external dependencies")
    print("6. Implement proper authentication and authorization")
    print("7. Add request validation and sanitization")
    print("8. Use structured logging for better debugging")
    print("9. Set up alerts for failures and anomalies")
    print("10. Regularly review and update security measures")


if __name__ == "__main__":
    main()
