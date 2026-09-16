"""
Agent with MCP Integration Example
This example demonstrates how to integrate Model Context Protocol (MCP) with Strands agents.
"""

from strands import Agent, tool
from typing import List, Dict


@tool
def search_files(query: str, file_type: str = "all") -> List[str]:
    """
    Search for files in a mock file system.
    This simulates MCP file search capabilities.
    
    Args:
        query: Search query
        file_type: Type of file to search for (all, txt, py, json)
        
    Returns:
        List of matching file paths
    """
    # Mock file system
    mock_files = {
        "all": [
            "/home/user/documents/report.txt",
            "/home/user/code/main.py",
            "/home/user/data/config.json",
            "/home/user/documents/notes.txt",
            "/home/user/code/utils.py"
        ],
        "txt": ["/home/user/documents/report.txt", "/home/user/documents/notes.txt"],
        "py": ["/home/user/code/main.py", "/home/user/code/utils.py"],
        "json": ["/home/user/data/config.json"]
    }
    
    files = mock_files.get(file_type, mock_files["all"])
    return [f for f in files if query.lower() in f.lower()]


@tool
def read_file_content(file_path: str) -> str:
    """
    Read the content of a file.
    This simulates MCP file reading capabilities.
    
    Args:
        file_path: Path to the file
        
    Returns:
        The file content
    """
    # Mock file contents
    mock_contents = {
        "/home/user/documents/report.txt": "This is a quarterly report with financial data.",
        "/home/user/code/main.py": "def main():\n    print('Hello, World!')\n\nif __name__ == '__main__':\n    main()",
        "/home/user/data/config.json": '{"api_key": "xxx", "timeout": 30}',
        "/home/user/documents/notes.txt": "Meeting notes: Discuss project timeline and deliverables.",
        "/home/user/code/utils.py": "def helper_function():\n    return 'Utility function'"
    }
    
    return mock_contents.get(file_path, "File not found")


@tool
def list_directory(path: str) -> List[str]:
    """
    List files in a directory.
    This simulates MCP directory listing capabilities.
    
    Args:
        path: Directory path
        
    Returns:
        List of files in the directory
    """
    # Mock directory structure
    mock_dirs = {
        "/home/user/documents": ["report.txt", "notes.txt"],
        "/home/user/code": ["main.py", "utils.py"],
        "/home/user/data": ["config.json"],
        "/home/user": ["documents/", "code/", "data/"]
    }
    
    return mock_dirs.get(path, ["Directory not found"])


@tool
def execute_command(command: str) -> str:
    """
    Execute a system command.
    This simulates MCP command execution capabilities.
    
    Args:
        command: The command to execute
        
    Returns:
        Command output
    """
    # Mock command outputs
    mock_outputs = {
        "ls": "file1.txt file2.py file3.json",
        "pwd": "/home/user",
        "whoami": "user",
        "date": "2024-01-15 10:30:00"
    }
    
    return mock_outputs.get(command, f"Executed: {command}")


def main():
    """
    Create an agent with MCP-like tools for file system operations.
    """
    print("=== Agent with MCP Integration Example ===\n")
    
    # Create an agent with MCP-like tools
    agent = Agent(tools=[search_files, read_file_content, list_directory, execute_command])
    
    # Queries that use MCP capabilities
    queries = [
        "Find all Python files in the system",
        "What's in the /home/user/documents directory?",
        "Read the content of /home/user/code/main.py",
        "Search for files containing 'report' and show me their content",
        "Execute the 'whoami' command"
    ]
    
    for query in queries:
        print(f"Query: {query}")
        response = agent(query)
        print(f"Agent: {response}\n")
        print("-" * 80 + "\n")


if __name__ == "__main__":
    main()
