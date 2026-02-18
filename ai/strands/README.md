# AWS Strands Python SDK Examples

This directory contains a comprehensive set of examples demonstrating how to use the AWS Strands Python SDK to build AI agents, ranging from simple conversational bots to complex autonomous systems.

## Overview

AWS Strands is a modern, model-driven open-source framework for building AI agents. It's designed to minimize boilerplate code and maximize flexibility, leveraging the reasoning capabilities of large language models (LLMs).

### Key Features

- **Lightweight, flexible agent loop** – Minimal code to get a basic agent working
- **Model agnostic** – Supports Amazon Bedrock (Claude, Titan, etc.), Anthropic, Llama, Gemini, OpenAI, and others
- **Powerful tool integration** – Tools are simple Python functions
- **Built-in MCP (Model Context Protocol)** – Access to thousands of prebuilt tools and services
- **Production ready** – Deployable on AWS or your own infrastructure

## Prerequisites

- Python 3.10 or higher
- AWS account with Bedrock access (for Bedrock examples)
- AWS CLI configured with appropriate permissions

## Installation

```bash
# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Strands SDK
pip install strands-agents strands-agents-tools

# For AWS Bedrock integration
pip install boto3
```

## Quick Start

You can run examples individually or use the interactive runner:

```bash
# Interactive menu
python run_examples.py

# Run a specific example by number
python run_examples.py 1

# Run a specific example by filename
python run_examples.py 01_basic_agent.py

# Or run examples directly
python 01_basic_agent.py
```

## Examples

### Basic Examples (01-03)

These examples cover the fundamental concepts of Strands agents:

#### 01. Basic Agent (`01_basic_agent.py`)
The simplest possible agent with no tools, demonstrating basic text interaction.

```bash
python 01_basic_agent.py
```

**What you'll learn:**
- Creating a basic Strands agent
- Simple query-response patterns
- Default LLM behavior

#### 02. Agent with Custom Tools (`02_agent_with_custom_tool.py`)
Learn how to create custom tools and integrate them with agents.

```bash
python 02_agent_with_custom_tool.py
```

**What you'll learn:**
- Creating custom tools with the `@tool` decorator
- Tool function documentation for LLM understanding
- Passing tools to agents
- Text processing capabilities

#### 03. Agent with Calculator (`03_agent_with_calculator.py`)
Mathematical operations using custom calculator tools.

```bash
python 03_agent_with_calculator.py
```

**What you'll learn:**
- Building domain-specific tools (math operations)
- Error handling in tools
- Multi-step problem solving

### Intermediate Examples (04-06)

These examples demonstrate more advanced agent capabilities:

#### 04. Multi-Tool Agent (`04_multi_tool_agent.py`)
An agent with multiple tools working together for complex tasks.

```bash
python 04_multi_tool_agent.py
```

**What you'll learn:**
- Combining different types of tools
- Agent decision-making with multiple tools
- Mock external API integration
- Temperature conversion and time utilities

#### 05. Agent with MCP Integration (`05_agent_with_mcp.py`)
Demonstrates Model Context Protocol integration for file system operations.

```bash
python 05_agent_with_mcp.py
```

**What you'll learn:**
- File system operations through MCP
- Directory listing and file reading
- Command execution simulation
- Search capabilities

#### 06. Agent with Memory (`06_agent_with_memory.py`)
Maintain conversation context and remember user preferences.

```bash
python 06_agent_with_memory.py
```

**What you'll learn:**
- Conversation memory implementation
- Storing and retrieving user preferences
- Conversation history tracking
- Stateful agent interactions

### Advanced Examples (07-09)

These examples showcase production-ready patterns and advanced architectures:

#### 07. Multi-Agent System (`07_multi_agent_system.py`)
Coordinate multiple specialized agents working together.

```bash
python 07_multi_agent_system.py
```

**What you'll learn:**
- Creating specialized agents (Research, Analysis, Writer)
- Agent coordination and communication
- Pipeline-based processing
- Complex workflow orchestration

#### 08. Agent with AWS Bedrock (`08_agent_with_bedrock.py`)
Integration with AWS Bedrock foundation models.

```bash
python 08_agent_with_bedrock.py
```

**What you'll learn:**
- AWS Bedrock configuration
- Model selection (Claude, Titan, Llama2)
- Text classification and entity extraction
- AWS credentials and permissions setup

**Prerequisites for this example:**
```bash
# Install AWS SDK
pip install boto3

# Configure AWS credentials
aws configure

# Set AWS region
export AWS_REGION=us-east-1
```

#### 09. Production-Ready Agent (`09_production_ready_agent.py`)
A fully production-ready agent with comprehensive error handling and monitoring.

```bash
python 09_production_ready_agent.py
```

**What you'll learn:**
- Error handling and recovery
- Rate limiting
- Logging and monitoring
- Metrics collection
- Production best practices

**Features demonstrated:**
- Custom decorators for monitoring
- Rate limiting to prevent abuse
- Comprehensive logging
- Performance metrics
- Graceful error handling

## Configuration

### Environment Variables

```bash
# For Bedrock integration
export AWS_REGION=us-east-1
export AWS_PROFILE=your-profile

# For other model providers
export OPENAI_API_KEY=your-key  # If using OpenAI
export ANTHROPIC_API_KEY=your-key  # If using Anthropic directly
```

### AWS Bedrock Setup

1. Enable model access in AWS Bedrock console
2. Configure IAM permissions for `bedrock:InvokeModel`
3. Set up AWS credentials using AWS CLI

```bash
aws configure
```

## Development Tips

### Creating Custom Tools

Tools are simple Python functions decorated with `@tool`:

```python
from strands import tool

@tool
def my_tool(param: str) -> str:
    """
    Clear description of what the tool does.
    This docstring helps the LLM understand when to use the tool.
    
    Args:
        param: Description of the parameter
        
    Returns:
        Description of the return value
    """
    return f"Processed: {param}"
```

### Best Practices

1. **Clear Documentation**: Write clear docstrings for all tools
2. **Type Hints**: Use proper type hints for parameters and returns
3. **Error Handling**: Implement proper error handling in tools
4. **Validation**: Validate inputs before processing
5. **Logging**: Add logging for debugging and monitoring
6. **Testing**: Test tools independently before integration

## Troubleshooting

### Common Issues

1. **Import Error**: Make sure `strands-agents` is installed
   ```bash
   pip install strands-agents strands-agents-tools
   ```

2. **AWS Credentials**: For Bedrock examples, ensure AWS credentials are configured
   ```bash
   aws sts get-caller-identity
   ```

3. **Model Access**: Verify Bedrock model access in AWS Console

4. **Rate Limits**: Be aware of rate limits for API calls

## Additional Resources

- [Official Documentation](https://strandsagents.com/latest/documentation/docs/)
- [GitHub Repository](https://github.com/strands-agents/sdk-python)
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [AWS Blog: Introducing Strands Agents](https://aws.amazon.com/blogs/opensource/introducing-strands-agents-an-open-source-ai-agents-sdk/)

## Contributing

Feel free to contribute additional examples or improvements to existing ones!

## License

These examples are provided for educational purposes. Please refer to the AWS Strands SDK license for usage terms.
