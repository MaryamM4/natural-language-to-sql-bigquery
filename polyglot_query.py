import pandas as pd
import json
from functools import lru_cache
import duckdb
import time

# True if: GCP project exists, BigQuery still enabled, 
# #        tables exists, and credentials  still valid.
BQ_ONLINE = False  

if BQ_ONLINE:
    from QueryRunner.bq_runner import BigQueryRunner
else:
    from QueryRunner.duckdb_runner import DuckDBRunner
    
# Helper reads results from file (waiting for model takes too long)
# Other than placeholder, SQL query results are AI-generated based on natural language prompts
@lru_cache(maxsize=1) # Cache file to avoid reloading every call
def load_queries():    
    file_path="bq_queries.json" if BQ_ONLINE else "csn_queries.json"

    with open(file_path, "r") as f:
        return json.load(f)

# Returns generated SQL query based on prompt & model selections
def get_query(question: str, model: str, prompt_label: str, file_path: str = "queries.json") -> str:
    data = load_queries()

    if question not in data:
        return "SELECT 'Error: Unknown Question'", "get_query error"
    if model not in data[question]:
        return "SELECT 'Error: Unknown Model'", "get_query error"
    if prompt_label not in data[question][model]:
        return "SELECT 'Error: Unknown Prompt Type'", "get_query error"

    return data[question][model][prompt_label], "success"

def save_results_report(results_log, question: str, output_filename="results", save_to_json:bool=False, sort_by: str = None):
    if not results_log:
        print("No results to save.")
        return

    if sort_by is not None: 
        try:
            results_log = sorted(results_log, key=lambda x: x.get("metrics", {}).get(sort_by, float("inf")))
        except Exception as e:
            print(f"save_results_report failed to sort by: {sort_by}.\n{e}\n")
    
    human_output_file = f"{output_filename}.md"
    engine = results_log[0].get("engine", "unknown")
    lines = []

    # Header
    lines.append(f"# Query Benchmark Report\n")
    lines.append(f"**Total Runs:** {len(results_log)}\n")
    lines.append(f"**Engine:**     {engine}")
    lines.append(f"**Question:**   {question}\n")

    # ----------------------------------
    lines.append("## Metrics\n")

    metric_keys = set()    # Collect all metric keys,
    for r in results_log:  # which may differ.
        if isinstance(r.get("metrics"), dict):
            metric_keys.update(r["metrics"].keys())

    metric_keys = sorted(metric_keys)

    # Header row
    header = ["Model", "Prompt", "Status"] + metric_keys
    lines.append("| " + " | ".join(header) + " |")
    lines.append("|" + " --- |" * len(header))

    # Rows
    for r in results_log:
        try:
            row = [r.get("model", "NA"), r.get("prompt", "NA"), r.get("status", "NA")]
        except Exception:
            row = ["NA"] * 3

        for k in metric_keys:
            try:
                val = r.get("metrics", {}).get(k, "NA") or {}
                if isinstance(val, float):
                    val = f"{val:.4f}"

            except Exception:
                val = "NA"
            row.append(str(val))

        lines.append("| " + " | ".join(row) + " |")

    # ----------------------------------
    lines.append("\n## Data Preview\n")

    lines.append("| Model | Prompt | Data Preview |")
    lines.append("| --- | --- | --- |")

    for r in results_log:
        try:
            model = r.get("model", "NA")
            prompt = r.get("prompt", "NA")
            preview = r.get("data_preview")

            if preview is None:
                preview_str = "NA"
            else:
                preview_str = str(preview).replace("\n", " ")[:200]

        except Exception:
            model = prompt = preview_str = "NA"

        lines.append(f"| {model} | {prompt} | {preview_str} |")

    # ----------------------------------
    lines.append("\n## Errors\n")

    lines.append("| (Model) Prompt | Status | Error Message |")
    lines.append("| --- | --- | --- |")

    has_errors = False

    for r in results_log:
        try:
            status = r.get("status", "NA")
            error = r.get("error")

            if status != "success" or (error not in [None, ""]):
                has_errors = True

                model = r.get("model", "NA")
                prompt = r.get("prompt", "NA")

                error_str = "NA" if error in [None, ""] else str(error).replace("\n", " ")[:200]

                lines.append(f"| ({model}) {prompt} | {status} | {error_str} |")

        except Exception:
            lines.append("| NA | NA | NA |")

    if not has_errors:
        lines.append("| NA | NA | No errors |")

    # ----------------------------------
    try:
        with open(human_output_file, "w") as f:  # Write readable file
            f.write("\n".join(lines))
    except Exception:
        print(f"Failed to write report to '{human_output_file}'.")
    
    if save_to_json:
        machine_out_file = f"{output_filename}.json"
        try:
            with open(machine_out_file, "w") as f: # Store for future use
                json.dump(results_log, f, indent=2)
        except Exception:
            print(f"Failed to write report to '{machine_out_file}'.")

    print(f"\nDone reporting to '{output_filename}'.")

def run_all_queries(question: str, runner, print_results: bool = True):
    data = load_queries()

    if question not in data:
        raise ValueError("Unknown question")

    results_log = []

    for model in data[question]:
        for prompt_label in data[question][model]:

            sql, status = get_query(question, model, prompt_label)
            sql = " ".join(sql.split()) # Normalize SQL
            
            error_mssg = None

            if print_results:
                print(f"\n{'='*60}")
                print(f"(Model: {model}) Prompt: {prompt_label}")
                print(f"SQL:\n{sql}\n")

            try:
                result = None

                if status == "success":
                    result, run_status = runner.run_query(sql)

                    # execution success decided HERE
                    engine = result.get("engine")
                    metrics = result.get("metrics")

                    data_preview = None
                    if result and isinstance(result.get("data"), pd.DataFrame):
                        df = result["data"]
                        data_preview = df.head(5).to_dict()

                    # display AFTER success is locked in
                    if print_results:
                        try:
                            runner.display_result_head(result, model, prompt_label)
                            runner.display_metrics(result)
                        except Exception as display_error:
                            print(f"(Display Error - ignored): {display_error}")

                engine = result.get("engine") if result else None
                metrics = result.get("metrics") if result else None

                data_preview = None # Avoid huge logs
                if result and result.get("data") is not None:
                    df = result["data"]
                    if isinstance(df, pd.DataFrame):
                        data_preview = df.head(5).to_dict()
                    else:
                        data_preview = str(df)[:500]

            except Exception as e:
                if print_results:
                    print(f"({model}) {prompt_label}:")
                    print(f"ERROR: {e}")
                
                metrics, data_preview = None, None
                engine = getattr(runner, "engine", "unknown")

                if run_status=="success":
                    status = "run_all_queries error"
                    error_mssg = str(e)
                
                else:
                    status = run_status
                    old_error = result.get("error")
                    error_mssg = f"{old_error}\n{str(e)}"
            
            results_log.append({"question": question, "model": model,  "prompt": prompt_label, "status": status,
                                "engine": engine,  "metrics": metrics,"data_preview": data_preview, "error": error_mssg})     


    return results_log

if __name__ == "__main__":
    question = "top_repos_question" # "Find repos with most python files."

    if BQ_ONLINE:
        runner = BigQueryRunner()
    else:
        runner = DuckDBRunner(mode="dHF_load")

    results_log = run_all_queries(question=question, runner=runner, print_results=True)

    performance_key = getattr(runner, "performance_key", "unknown")
    save_results_report(results_log, question, save_to_json=True, sort_by=runner.performance_key)