from google.cloud import bigquery
import pandas as pd

def ask_genai_for_sql(question):
    # Simulated AI response for "most python files"
    if "python" in question.lower():
        return """
        SELECT repo_name, COUNT(DISTINCT path) as count
        FROM `bigquery-public-data.github_repos.sample_files`
        WHERE path LIKE '%.py'
        GROUP BY repo_name
        ORDER BY count DESC
        LIMIT 5
        """
    return "SELECT 'Error: Unknown Question'"

def execute_bq(sql):
    client = bigquery.Client()
    query_job = client.query(sql)
    return query_job.to_dataframe()

if __name__ == "__main__":
    q = "Find repos with most python files"
    print(f"User Question: {q}")
    
    sql = ask_genai_for_sql(q)
    print(f"Generated SQL: {sql}")
    
    df = execute_bq(sql)
    print("Results:")
    print(df)
