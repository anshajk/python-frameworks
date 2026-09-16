#!/usr/bin/env python3
"""
Run All Strands Examples
This script allows you to run all or specific Strands examples easily.
"""

import sys
import subprocess
from pathlib import Path


EXAMPLES = {
    "basic": [
        ("01_basic_agent.py", "Basic Agent - Simple text interaction"),
        ("02_agent_with_custom_tool.py", "Custom Tools - Text processing tools"),
        ("03_agent_with_calculator.py", "Calculator - Math operations"),
    ],
    "intermediate": [
        ("04_multi_tool_agent.py", "Multi-Tool Agent - Weather, calculator, time"),
        ("05_agent_with_mcp.py", "MCP Integration - File system operations"),
        ("06_agent_with_memory.py", "Memory - Conversation history"),
    ],
    "advanced": [
        ("07_multi_agent_system.py", "Multi-Agent System - Coordinated agents"),
        ("08_agent_with_bedrock.py", "AWS Bedrock - Foundation models"),
        ("09_production_ready_agent.py", "Production Ready - Full monitoring"),
    ],
}


def print_menu():
    """Print the examples menu."""
    print("\n" + "=" * 80)
    print("AWS Strands SDK Examples Runner")
    print("=" * 80 + "\n")
    
    print("Basic Examples:")
    for i, (file, desc) in enumerate(EXAMPLES["basic"], 1):
        print(f"  {i}. {desc}")
    
    print("\nIntermediate Examples:")
    for i, (file, desc) in enumerate(EXAMPLES["intermediate"], 4):
        print(f"  {i}. {desc}")
    
    print("\nAdvanced Examples:")
    for i, (file, desc) in enumerate(EXAMPLES["advanced"], 7):
        print(f"  {i}. {desc}")
    
    print("\nOptions:")
    print("  10. Run all basic examples")
    print("  11. Run all intermediate examples")
    print("  12. Run all advanced examples")
    print("  13. Run all examples")
    print("  0. Exit")
    print()


def run_example(filename):
    """Run a specific example."""
    script_dir = Path(__file__).parent
    example_path = script_dir / filename
    
    if not example_path.exists():
        print(f"Error: {filename} not found!")
        return False
    
    print("\n" + "=" * 80)
    print(f"Running: {filename}")
    print("=" * 80 + "\n")
    
    try:
        result = subprocess.run(
            [sys.executable, str(example_path)],
            cwd=script_dir,
            capture_output=False
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error running {filename}: {e}")
        return False


def run_all_in_category(category):
    """Run all examples in a category."""
    examples = EXAMPLES.get(category, [])
    print(f"\n{'='*80}")
    print(f"Running all {category} examples")
    print('='*80)
    
    for filename, desc in examples:
        run_example(filename)
        print("\n" + "-" * 80 + "\n")


def main():
    """Main function."""
    if len(sys.argv) > 1:
        # Run specific example from command line
        example_num = sys.argv[1]
        if example_num.isdigit():
            num = int(example_num)
            all_examples = EXAMPLES["basic"] + EXAMPLES["intermediate"] + EXAMPLES["advanced"]
            if 1 <= num <= len(all_examples):
                filename, _ = all_examples[num - 1]
                run_example(filename)
                return
        
        # Or run by filename
        if sys.argv[1].endswith(".py"):
            run_example(sys.argv[1])
            return
    
    # Interactive mode
    while True:
        print_menu()
        choice = input("Select an example to run (0-13): ").strip()
        
        if not choice.isdigit():
            print("Invalid choice. Please enter a number.")
            continue
        
        choice = int(choice)
        
        if choice == 0:
            print("Goodbye!")
            break
        elif choice == 10:
            run_all_in_category("basic")
        elif choice == 11:
            run_all_in_category("intermediate")
        elif choice == 12:
            run_all_in_category("advanced")
        elif choice == 13:
            for category in ["basic", "intermediate", "advanced"]:
                run_all_in_category(category)
        elif 1 <= choice <= 9:
            all_examples = EXAMPLES["basic"] + EXAMPLES["intermediate"] + EXAMPLES["advanced"]
            filename, _ = all_examples[choice - 1]
            run_example(filename)
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
