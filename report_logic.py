import pandas as pd

def generate_summary_report(file_path):
    # Read Excel
    df = pd.read_excel(file_path)

    # Example: Summarize numeric columns
    summary = df.describe()

    # Save report as Excel
    output_file = "summary_report.xlsx"
    summary.to_excel(output_file)

    return output_file
