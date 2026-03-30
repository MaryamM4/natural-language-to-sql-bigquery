from .query_runner import QueryRunner
from google.cloud import bigquery

class BigQueryRunner(QueryRunner):
    def __init__(self):
        self.client = bigquery.Client()
        self.engine = "bigquery"
        self.performance_key = "elapsed_time_sec"
    
    def run_query(self, sql: str):
        status = "success" # TODO
        job = self.client.query(sql)
        df = job.to_dataframe()

        return {
            "engine": self.engine,
            "data": df,
            "metrics": {
                "bytes_processed": job.total_bytes_processed,
                "bytes_billed": job.total_bytes_billed,
                "elapsed_time_sec": (job.ended - job.started).total_seconds()
            }
        }, status 

    def display_metrics(self, result):
        m = result["metrics"]

        print("\n--- BigQuery Metrics ---")
        print(f"Bytes Processed: {m['bytes_processed']}")
        print(f"Bytes Billed: {m['bytes_billed']}")
        print(f"Elapsed Time: {m['elapsed_time_sec']:.4f}s")