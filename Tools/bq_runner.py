from .query_runner import QueryRunner, QueryResult
from google.cloud import bigquery

class BigQueryRunner(QueryRunner):
    def __init__(self):
        self.client = bigquery.Client()
        self.engine = "bigquery"
        self.performance_key = "elapsed_time_sec"
    
    def run_query(self, sql: str) -> QueryResult:
        result = QueryResult(sql=sql, status="success", engine=self.engine,
            data=None, metrics={}, profile=None, error=None)

        try:
            job = self.client.query(sql)
            df = job.to_dataframe()
            result.data = df

            result.metrics = {
                "bytes_processed": job.total_bytes_processed,
                "bytes_billed": job.total_bytes_billed,
                "elapsed_time_sec": (job.ended - job.started).total_seconds()
            }

            # BigQuery doesn't expose a full EXPLAIN ANALYZE profile like DuckDB, 
            result.profile = getattr(job, "query_plan", None) # but job might have some details

        except Exception as e:
            result.error = str(e)
            result.status = "bigquery run_query error"

        return result

    def display_metrics(self, result: QueryResult):
        m = result.metrics
        print("\n--- BigQuery Metrics ---")
        print(f"Bytes Processed: {m['bytes_processed']}")
        print(f"Bytes Billed: {m['bytes_billed']}")
        print(f"Elapsed Time: {m['elapsed_time_sec']:.4f}s")
    
    def display_metrics(self, result: QueryResult):
        print("\n--- BigQuery Metrics ---")

        m = result.metrics
        if m is None:
            print("No metrics.")
            return
        
        bytes_processed = m.get("bytes_processed") or "NA"
        bytes_billed = m.get("bytes_billed") or "NA"
        elapsed_time = m.get("elapsed_time_sec") or "NA"

        print(f"Bytes Processed: {bytes_processed}")
        print(f"Bytes Billed: {bytes_billed}")
        print(f"Elapsed Time: {elapsed_time}s")
