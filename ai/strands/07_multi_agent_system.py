"""
Multi-Agent System Example
This example demonstrates how to coordinate multiple specialized agents working together.
"""

from strands import Agent, tool
from typing import Dict, List
import json


# Research Agent Tools
@tool
def search_database(query: str) -> List[Dict]:
    """
    Search a mock database for information.
    
    Args:
        query: The search query
        
    Returns:
        List of matching records
    """
    # Mock database
    database = [
        {"id": 1, "topic": "AI", "content": "Artificial Intelligence is transforming industries"},
        {"id": 2, "topic": "ML", "content": "Machine Learning enables computers to learn from data"},
        {"id": 3, "topic": "DL", "content": "Deep Learning uses neural networks with multiple layers"},
        {"id": 4, "topic": "NLP", "content": "Natural Language Processing helps computers understand human language"},
        {"id": 5, "topic": "CV", "content": "Computer Vision enables machines to interpret visual information"}
    ]
    
    return [rec for rec in database if query.lower() in rec["topic"].lower() or query.lower() in rec["content"].lower()]


@tool
def summarize_research(data: str) -> str:
    """
    Create a summary of research data.
    
    Args:
        data: The data to summarize
        
    Returns:
        A summary
    """
    return f"Summary: {data[:100]}..." if len(data) > 100 else f"Summary: {data}"


# Analysis Agent Tools
@tool
def analyze_sentiment(text: str) -> str:
    """
    Analyze the sentiment of text.
    
    Args:
        text: The text to analyze
        
    Returns:
        Sentiment analysis result
    """
    # Simple mock sentiment analysis
    positive_words = ["good", "great", "excellent", "amazing", "wonderful", "transforming"]
    negative_words = ["bad", "poor", "terrible", "awful", "horrible"]
    
    text_lower = text.lower()
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)
    
    if pos_count > neg_count:
        return "Positive sentiment detected"
    elif neg_count > pos_count:
        return "Negative sentiment detected"
    else:
        return "Neutral sentiment detected"


@tool
def extract_keywords(text: str) -> List[str]:
    """
    Extract keywords from text.
    
    Args:
        text: The text to analyze
        
    Returns:
        List of keywords
    """
    # Simple keyword extraction (mock)
    common_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "is"}
    words = text.lower().split()
    keywords = [w for w in words if len(w) > 3 and w not in common_words]
    return list(set(keywords))[:5]  # Return top 5 unique keywords


# Writer Agent Tools
@tool
def generate_report(data: str, format: str = "markdown") -> str:
    """
    Generate a formatted report.
    
    Args:
        data: The data to include in the report
        format: The format (markdown, html, text)
        
    Returns:
        Formatted report
    """
    if format == "markdown":
        return f"# Report\n\n## Content\n\n{data}\n\n---\nGenerated automatically"
    elif format == "html":
        return f"<html><body><h1>Report</h1><p>{data}</p></body></html>"
    else:
        return f"Report\n{'='*50}\n{data}\n{'='*50}"


@tool
def format_list(items: List[str], style: str = "bullet") -> str:
    """
    Format a list of items.
    
    Args:
        items: List of items
        style: The style (bullet, numbered, comma)
        
    Returns:
        Formatted list
    """
    if style == "bullet":
        return "\n".join([f"• {item}" for item in items])
    elif style == "numbered":
        return "\n".join([f"{i+1}. {item}" for i, item in enumerate(items)])
    else:
        return ", ".join(items)


class MultiAgentSystem:
    """Coordinate multiple specialized agents."""
    
    def __init__(self):
        # Create specialized agents
        self.research_agent = Agent(
            tools=[search_database, summarize_research],
            name="ResearchAgent"
        )
        
        self.analysis_agent = Agent(
            tools=[analyze_sentiment, extract_keywords],
            name="AnalysisAgent"
        )
        
        self.writer_agent = Agent(
            tools=[generate_report, format_list],
            name="WriterAgent"
        )
    
    def process_task(self, task: str) -> Dict[str, str]:
        """
        Process a task using multiple agents in coordination.
        
        Args:
            task: The task description
            
        Returns:
            Results from each agent
        """
        results = {}
        
        # Step 1: Research Agent gathers information
        print("ResearchAgent working...")
        research_result = self.research_agent(f"Find information about: {task}")
        results["research"] = research_result
        
        # Step 2: Analysis Agent analyzes the research
        print("AnalysisAgent working...")
        analysis_result = self.analysis_agent(f"Analyze this: {research_result}")
        results["analysis"] = analysis_result
        
        # Step 3: Writer Agent creates final output
        print("WriterAgent working...")
        writer_result = self.writer_agent(
            f"Create a report based on this research: {research_result} and analysis: {analysis_result}"
        )
        results["report"] = writer_result
        
        return results


def main():
    """
    Demonstrate multi-agent coordination.
    """
    print("=== Multi-Agent System Example ===\n")
    
    # Create the multi-agent system
    system = MultiAgentSystem()
    
    # Tasks for the multi-agent system
    tasks = [
        "artificial intelligence",
        "machine learning applications",
        "natural language processing"
    ]
    
    for task in tasks:
        print(f"\n{'='*80}")
        print(f"Task: {task}")
        print('='*80 + "\n")
        
        results = system.process_task(task)
        
        print("\n--- Results ---")
        for agent_name, result in results.items():
            print(f"\n{agent_name.upper()}:")
            print(result)
            print("-" * 80)


if __name__ == "__main__":
    main()
