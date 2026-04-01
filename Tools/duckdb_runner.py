from .query_runner import QueryRunner, QueryResult
import duckdb
import time
import os
import pandas as pd
import json

'''

duckdb missing support for tracking runtime metrics:
- rows scanned
- intermediate rows
- memory usage
- execution time
'''

# For dHFing Hugging Face datasets
dHF_N_ROWS = 200
HF_DATASET = "code_search_net"
try: 
    from datasets import load_dataset
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False

class DuckDBRunner(QueryRunner):
    """
    DuckDB runner has the following data modes (strings):
    - dHF:        Downloads a small subset (dHF_N_ROWS) from Hugging Face 
    - dHF_save:   dHF, but also save to local file
    - dHF_load:   dHF, but use saved local file
    - synthetic:  Creates a small fake table locally (default)
    - local:      Uses existing Parquet file
    """

    def __init__(self, db_path:str = ":memory:", mode:str = "synthetic"):
        self.con = duckdb.connect(db_path)
        self.con.execute("PRAGMA enable_profiling='json';")
        self.con.execute("PRAGMA profiling_output='duckdb_profile.json';")
        # File is overwritten per query (fine for use case), 
        # but note it's not thread-safe nor parallel-safe

        self.engine = "duckdb"
        self.performance_key = "execution_time_avg"
        self.mode = mode
        self.table_name = "sample_files"

        # Initialize the dataset according to mode
        if mode == "synthetic":
            self._create_synthetic_table()
        elif mode == "local":
            self._load_local_parquet()

        elif mode == "dHF" or mode == "dHF_save" or mode == "dHF_load":
            if not HF_AVAILABLE:
                raise ImportError("Hugging Face datasets not installed. Install via `pip install datasets`")
            self._load_hf_subset(mode=mode)

        else:
            raise ValueError(f"Unknown mode: {mode}")

    # -------------------------------------
    # (1) Mode Helpers

    # Creates a small synthetic dataset similar to GitHub files.
    def _create_synthetic_table(self):
        df = pd.DataFrame({"repo_name": [f"repo_{i}" for i in range(1, 11)], "path": [f"file_{i}.py" for i in range(1, 11)]})

        self.con.register("tmp_df", df)
        self.con.execute(f"CREATE OR REPLACE TABLE {self.table_name} AS SELECT * FROM tmp_df")

        print(f"[DuckDBRunner] Synthetic table '{self.table_name}' created with {len(df)} rows.")

    # Loads a local Parquet file into DuckDB, if available.
    def _load_local_parquet(self, parquet_path:str = "data/sample_files.parquet"):
        if not os.path.exists(parquet_path):
            raise FileNotFoundError(f"Parquet file not found at {parquet_path}")
        
        self.con.execute(f"CREATE OR REPLACE TABLE {self.table_name} AS SELECT * FROM '{parquet_path}'")
        print(f"[DuckDBRunner] Loaded local Parquet into table '{self.table_name}'.")

    # dHFs a small subset from Hugging Face and create a DuckDB table. Has option to save as Parquet
    def _load_hf_subset(self, mode:str, hf_dataset:str = HF_DATASET, n_samples:int = dHF_N_ROWS, parquet_path:str = "data/hf_sample_files.parquet"):
        if mode == "dHF_load":
            if os.path.exists(parquet_path):
                print(f"[DuckDBRunner] Loading Hugging Face dataset from local file '{parquet_path}'...")
                self.con.execute(f"CREATE OR REPLACE TABLE {self.table_name} AS SELECT * FROM '{parquet_path}'")
                print(f"[DuckDBRunner] Table '{self.table_name}' loaded from Parquet with DuckDB.")
                return
            
            else:
                print(f"[DuckDBRunner] Parquet file not found at '{parquet_path}', falling back to dHF_save mode...")
                mode = "dHF_save"  # fallback to download & save

        print(f"[DuckDBRunner] Downloading {n_samples} samples from Hugging Face dataset '{hf_dataset}'...")
        ds = load_dataset(hf_dataset, "python", split=f"train[:{n_samples}]")
        df = pd.DataFrame(ds)

        # Map the columns dynamically for code_search_net
        if all(col in df.columns for col in ["repository_name", "func_path_in_repository"]):
            table_df = df[["repository_name", "func_path_in_repository"]].copy()

            table_df = df.rename(columns={
                "repository_name": "repo_name",
                "func_path_in_repository": "path",
                "func_code_string": "code",
            })[["repo_name", "path", "func_name", "language", "code"]]


        elif "code" in df.columns:  # fallback for other datasets
            table_df = df.rename(columns={"code": "path"})
            table_df["repo_name"] = ["repo_" + str(i) for i in range(len(df))]
            table_df = table_df[["repo_name", "path"]]
        else:
            raise ValueError(f"Unexpected dataset columns: {df.columns.tolist()}")
        
        #if 'language' not in table_df.columns: # Create default/dummy language column
        #    table_df['language'] = 'python'    # for COT-style queries to work

        self.con.register("tmp_df", table_df)  # Register in DuckDB
        self.con.execute(f"CREATE OR REPLACE TABLE {self.table_name} AS SELECT * FROM tmp_df")
        print(f"[DuckDBRunner] Table '{self.table_name}' created with {len(table_df)} rows.")

        if mode == "dHF_save":
            os.makedirs(os.path.dirname(parquet_path), exist_ok=True)
            table_df.to_parquet(parquet_path, index=False)
            print(f"[DuckDBRunner] Hugging Face dataset saved locally at '{parquet_path}'")

        print()

    # (1) Mode Helpers END
    # -------------------------------------

    # -------------------------------------
    # (2) Metric Helpers

    def _extract_plan_metrics(self, profile_path:str = "duckdb_profile.json") -> dict:
        if not os.path.exists(profile_path):
            return {}

        try:
            with open(profile_path, "r") as f:
                profile = json.load(f)

            def traverse(node, depth=0):
                operator_count = 1
                max_depth = depth
                rows = node.get("cardinality", 0)
                time = node.get("timing", 0)

                children = node.get("children", [])

                for child in children:
                    c_count, c_depth, c_rows, c_time = traverse(child, depth + 1)
                    operator_count += c_count
                    max_depth = max(max_depth, c_depth)
                    rows += c_rows
                    time += c_time

                return operator_count, max_depth, rows, time

            root = profile.get("result", {})
            op_count, depth, total_rows, total_time = traverse(root)

            return {
                "actual_operator_count": op_count,
                "actual_plan_depth": depth,
                "total_rows_processed": total_rows,
                "total_operator_time": total_time
            }

        except Exception as e:
            return {
                "actual_operator_count": None,
                "actual_plan_depth": None,
                "total_rows_processed": None,
                "total_operator_time": None,
                "profile_error": str(e)
            }

    # (2) Metric Helpers END
    # -------------------------------------

    def run_query(self, sql: str, runs:int = 5) -> QueryResult:
        result = QueryResult(sql=sql, status="success", engine=self.engine,
                             data=None, metrics={}, profile=None, error=None)
        
        times = [] # DuckDB doesn't track

        try:
            self.con.execute(sql).fetchall()          # Warmup
            result.data = self.con.execute(sql).df() # First run, for data

            for _ in range(runs): # Timed runs
                start = time.time()
                self.con.execute(sql).fetchall()
                times.append(time.time() - start)

            result.profile = self.con.execute("EXPLAIN ANALYZE " + sql).fetchall() # Query plan / profile
            plan_metrics = self._extract_plan_metrics()                           
            result.metrics = {                                                     # Execution metrics
                "execution_time_min": min(times) if times else None,
                "execution_time_avg": (sum(times) / len(times)) if times else None,
                "execution_time_max": max(times) if times else None,
                **plan_metrics
            }

        except Exception as e:
            result.error = str(e)
            result.status = "duckdb run_query error"
        
        return result

    def display_metrics(self, result: QueryResult): 
        m = result.metrics or {} 
        
        print("\n--- DuckDB Metrics ---") 
        min_t = m.get("execution_time_min") 
        avg_t = m.get("execution_time_avg") 
        max_t = m.get("execution_time_max") 
        
        print(f"Min: {min_t:.4f}s" if min_t is not None else "Min: NA") 
        print(f"Avg: {avg_t:.4f}s" if avg_t is not None else "Avg: NA") 
        print(f"Max: {max_t:.4f}s" if max_t is not None else "Max: NA") 
        
        print("\n--- Query Plan ---") 
        if result.profile:
            for row in result.profile: 
                print(row) 
        else: 
            print("Profile DNE.")