import os
import time
import requests
from openai import OpenAI
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def create_sample_csv():
    """Create a sample CSV file with sales data for analysis"""
    # Generate sample sales data
    np.random.seed(42)

    dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
    n_days = len(dates)

    # Create seasonal pattern
    seasonal_pattern = np.sin(np.arange(n_days) * 2 * np.pi / 365) * 20 + 100

    # Add some noise and trend
    trend = np.linspace(0, 30, n_days)
    noise = np.random.normal(0, 10, n_days)

    # Generate sales data
    sales_data = {
        "date": dates,
        "product_a_sales": seasonal_pattern
        + trend
        + noise
        + np.random.normal(0, 5, n_days),
        "product_b_sales": seasonal_pattern * 0.8
        + trend * 1.2
        + np.random.normal(0, 8, n_days),
        "product_c_sales": seasonal_pattern * 1.2
        + trend * 0.8
        + np.random.normal(0, 12, n_days),
        "marketing_spend": np.abs(np.random.normal(1000, 300, n_days)),
        "website_visits": np.abs(
            seasonal_pattern * 50 + trend * 10 + np.random.normal(0, 500, n_days)
        ),
        "customer_satisfaction": np.clip(4 + np.random.normal(0, 0.5, n_days), 1, 5),
    }

    df = pd.DataFrame(sales_data)

    # Add derived columns
    df["total_sales"] = (
        df["product_a_sales"] + df["product_b_sales"] + df["product_c_sales"]
    )
    df["conversion_rate"] = df["total_sales"] / df["website_visits"] * 100
    df["month"] = df["date"].dt.month
    df["quarter"] = df["date"].dt.quarter
    df["day_of_week"] = df["date"].dt.day_name()

    # Save to CSV
    csv_path = Path("sales_data_2023.csv")
    df.to_csv(csv_path, index=False)
    print(f"Created sample CSV: {csv_path}")

    return csv_path


def download_file(file_id, filename):
    """Download a file from OpenAI"""
    try:
        file_content = client.files.content(file_id)

        # Save the file
        output_path = Path("generated_plots") / filename
        output_path.parent.mkdir(exist_ok=True)

        with open(output_path, "wb") as f:
            f.write(file_content.content)

        print(f"Downloaded: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error downloading file: {e}")
        return None


def demonstrate_code_interpreter():
    """Demonstrate code interpreter capability with data analysis"""
    print("=== OpenAI Code Interpreter Demonstration ===\n")

    # Create sample data
    print("Creating sample sales data...")
    csv_path = create_sample_csv()
    print()

    try:
        # Upload the CSV file
        print("Uploading CSV file to OpenAI...")
        with open(csv_path, "rb") as f:
            uploaded_file = client.files.create(file=f, purpose="assistants")
        print(f"File uploaded with ID: {uploaded_file.id}")
        print()

        # Create an assistant with code interpreter
        print("Creating assistant with code interpreter...")
        assistant = client.beta.assistants.create(
            name="Data Analysis Assistant",
            instructions="""You are a data analyst assistant. Analyze the provided CSV file and:
1. Provide a summary of the data
2. Identify key trends and patterns
3. Create visualizations to support your findings
4. Generate insights and recommendations

Always create high-quality visualizations with proper labels, titles, and legends.""",
            model="gpt-4.1",
            tools=[{"type": "code_interpreter"}],
            tool_resources={"code_interpreter": {"file_ids": [uploaded_file.id]}},
        )

        # Create a thread
        thread = client.beta.threads.create()

        # Analysis request
        analysis_request = """Please analyze the sales data CSV file and:

1. **Data Overview**: Provide a summary of the dataset structure and basic statistics
2. **Trend Analysis**: Identify sales trends over time for each product
3. **Seasonal Patterns**: Analyze any seasonal patterns in the data
4. **Correlation Analysis**: Examine relationships between variables (sales, marketing spend, website visits)
5. **Performance Metrics**: Calculate key metrics like average sales, growth rates, and conversion rates

Please create the following visualizations:
- Line plot showing monthly sales trends for all products
- Heatmap showing correlation between variables
- Bar chart comparing quarterly sales performance
- Scatter plot of marketing spend vs total sales
- Box plot showing sales distribution by day of week

Save all plots as high-resolution images and provide insights for each visualization."""

        print("Sending analysis request...")
        print("-" * 50)

        # Send the analysis request
        message = client.beta.threads.messages.create(
            thread_id=thread.id, role="user", content=analysis_request
        )

        # Run the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread.id, assistant_id=assistant.id
        )

        # Wait for completion with status updates
        print("Processing analysis...")
        while run.status not in ["completed", "failed"]:
            time.sleep(2)
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            print(f"Status: {run.status}")

            if run.status == "failed":
                print(f"Run failed: {run.last_error}")
                break

        print()

        # Get the response
        if run.status == "completed":
            messages = client.beta.threads.messages.list(
                thread_id=thread.id, order="desc"
            )

            # Process the response
            for message in reversed(messages.data):
                if message.role == "assistant":
                    print("Assistant Response:")
                    print("=" * 50)

                    # Process each content item
                    for content in message.content:
                        if content.type == "text":
                            print(content.text.value)
                            print()
                        elif content.type == "image_file":
                            # Download the image
                            file_id = content.image_file.file_id
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            filename = f"plot_{timestamp}_{file_id[-8:]}.png"
                            download_file(file_id, filename)

            # List all generated files
            print("\nGenerated Files:")
            print("-" * 30)
            generated_dir = Path("generated_plots")
            if generated_dir.exists():
                for file in generated_dir.glob("*.png"):
                    print(f"  - {file.name}")

        # Cleanup
        print("\n\nCleaning up...")
        client.beta.assistants.delete(assistant.id)
        client.files.delete(uploaded_file.id)
        print("Cleanup completed.")

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()


def main():
    demonstrate_code_interpreter()


if __name__ == "__main__":
    main()
