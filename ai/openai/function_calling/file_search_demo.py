import os
import time
from openai import OpenAI
from pathlib import Path
import json

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def create_sample_files():
    """Create sample text files for demonstration"""
    sample_dir = Path("sample_documents")
    sample_dir.mkdir(exist_ok=True)

    # Create sample documents
    documents = {
        "python_guide.txt": """Python Programming Guide
        
Python is a high-level, interpreted programming language known for its simplicity and readability.

Key Features:
- Dynamic typing
- Automatic memory management
- Extensive standard library
- Cross-platform compatibility

Common Use Cases:
1. Web development (Django, Flask)
2. Data science (NumPy, Pandas, Scikit-learn)
3. Machine learning (TensorFlow, PyTorch)
4. Automation and scripting
5. GUI development (Tkinter, PyQt)

Best Practices:
- Follow PEP 8 style guide
- Use virtual environments
- Write comprehensive tests
- Document your code
""",
        "data_science_overview.txt": """Data Science Overview

Data science combines statistics, mathematics, and computer science to extract insights from data.

Key Components:
1. Data Collection and Cleaning
2. Exploratory Data Analysis (EDA)
3. Feature Engineering
4. Model Building
5. Model Evaluation and Deployment

Popular Tools:
- Python: Pandas, NumPy, Matplotlib, Seaborn
- R: ggplot2, dplyr, tidyr
- SQL for database queries
- Jupyter Notebooks for interactive analysis

Machine Learning Algorithms:
- Supervised Learning: Linear Regression, Decision Trees, Random Forests
- Unsupervised Learning: K-Means, DBSCAN, PCA
- Deep Learning: Neural Networks, CNNs, RNNs
""",
        "api_documentation.txt": """API Documentation Best Practices

Well-documented APIs are crucial for developer adoption and success.

Essential Components:
1. Authentication methods
2. Endpoint descriptions
3. Request/response examples
4. Error codes and handling
5. Rate limiting information

Documentation Tools:
- Swagger/OpenAPI
- Postman
- ReadMe
- Docusaurus

Example API Response:
{
    "status": "success",
    "data": {
        "id": 123,
        "name": "Sample Item",
        "created_at": "2024-01-15T10:30:00Z"
    },
    "meta": {
        "page": 1,
        "total": 100
    }
}
""",
    }

    file_paths = []
    for filename, content in documents.items():
        file_path = sample_dir / filename
        file_path.write_text(content)
        file_paths.append(str(file_path))
        print(f"Created: {file_path}")

    return file_paths


def demonstrate_file_search():
    """Demonstrate file search capability with OpenAI Assistant"""
    print("=== OpenAI File Search Demonstration ===\n")

    # Create sample files
    print("Creating sample documents...")
    file_paths = create_sample_files()
    print()

    try:
        # Create a vector store
        print("Creating vector store...")
        vector_store = client.vector_stores.create(name="Technical Documentation Store")

        # Upload files to the vector store
        print("Uploading files to vector store...")
        file_streams = []
        for path in file_paths:
            file_streams.append(open(path, "rb"))

        file_batch = client.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id, files=file_streams
        )

        # Close file streams
        for stream in file_streams:
            stream.close()

        print(f"Files uploaded: {file_batch.file_counts}")
        print()

        # Create an assistant with file search capability
        print("Creating assistant with file search capability...")
        assistant = client.beta.assistants.create(
            name="Documentation Assistant",
            instructions="You are a helpful assistant that can search through technical documentation to answer questions.",
            model="gpt-4-turbo-preview",
            tools=[{"type": "file_search"}],
            tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
        )

        # Create a thread
        thread = client.beta.threads.create()

        # Example queries
        queries = [
            "What are the best practices for Python programming mentioned in the documents?",
            "What machine learning algorithms are discussed in the data science overview?",
            "How should API responses be structured according to the documentation?",
        ]

        for query in queries:
            print(f"\nQuery: {query}")
            print("-" * 50)

            # Add message to thread
            message = client.beta.threads.messages.create(
                thread_id=thread.id, role="user", content=query
            )

            # Run the assistant
            run = client.beta.threads.runs.create(
                thread_id=thread.id, assistant_id=assistant.id
            )

            # Wait for completion
            while run.status != "completed":
                time.sleep(1)
                run = client.beta.threads.runs.retrieve(
                    thread_id=thread.id, run_id=run.id
                )
                if run.status == "failed":
                    print(f"Run failed: {run.last_error}")
                    break

            # Get the response
            if run.status == "completed":
                messages = client.beta.threads.messages.list(
                    thread_id=thread.id, order="desc", limit=1
                )

                response = messages.data[0].content[0].text.value
                print(f"Assistant: {response}")

        # Cleanup
        print("\n\nCleaning up...")
        client.beta.assistants.delete(assistant.id)
        client.vector_stores.delete(vector_store.id)
        print("Cleanup completed.")

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()


def main():
    demonstrate_file_search()


if __name__ == "__main__":
    main()
