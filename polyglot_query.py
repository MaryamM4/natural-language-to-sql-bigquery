import pandas as pd
import json
from functools import lru_cache
import duckdb
import time
from Tools.sql_query_analyzer import SQLComplexityAnalyzer

# True if: GCP project exists, BigQuery still enabled, 
# #        tables exists, and credentials  still valid.
BQ_ONLINE = False  

if BQ_ONLINE:
    from Tools.bq_runner import BigQueryRunner
else:
    from Tools.duckdb_runner import DuckDBRunner
    
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

def save_results_report(results_log, question: str, output_filename="results", save_to_json:bool=False, sort_by: str = None, feature_priority = ["complexity_score"]):
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
    lines.append(f"**Engine:**     {engine}\n")
    lines.append(f"**Question:**   {question}\n")

    # ----------------------------------
    lines.append("## Metrics\n")

    metric_keys = set()    # Collect all metric keys.
    for r in results_log:
        if isinstance(r.get("metrics"), dict):
            for k in r["metrics"].keys():
                if k in SQLComplexityAnalyzer.FEATURE_KEYS:
                    continue
                if k in SQLComplexityAnalyzer.ANTIPATTERN_KEYS:
                    continue
                metric_keys.add(k)

    metric_keys.discard("antipattern_penalty") # force last
    metric_keys = sorted(metric_keys)
    metric_keys.append("antipattern_penalty")  # Not rlly part of metrics but handy here

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
                val = r.get("metrics", {}).get(k, "NA")

                if val is None:
                    val = "NA"
                elif isinstance(val, float):
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
    lines.append("\n## Features\n")
    
    feature_keys = sorted(k for k in SQLComplexityAnalyzer.FEATURE_KEYS if k not in feature_priority) + feature_priority
    feature_keys.append("complexity_score")  # force last column

    lines.append("| Model | Prompt | " + " | ".join(feature_keys) + " |")
    lines.append("| --- | --- |" + " --- |" * len(feature_keys))

    for r in results_log:
        try:
            model = r.get("model", "NA")
            prompt = r.get("prompt", "NA")
            metrics = r.get("metrics", {})

            row = [model, prompt]

            for k in feature_keys:
                val = metrics.get(k, "NA")
                if isinstance(val, float):
                    val = f"{val:.4f}"
                row.append(str(val))

            lines.append("| " + " | ".join(row) + " |")

        except Exception:
            lines.append("| NA | NA | NA |")
    
    # ----------------------------------
    lines.append("\n## Antipatterns\n")

    lines.append("| (Model) Prompt | Antipatterns Detected | Penalty |")
    lines.append("| --- | --- | --- |")

    has_antipatterns = False

    for r in results_log:
        try:
            metrics = r.get("metrics", {})
            detected = [ # extract boolean antipattern flags
                k for k in SQLComplexityAnalyzer.ANTIPATTERN_KEYS
                if metrics.get(k) is True
            ]

            if not detected:
                continue  # skip rows without antipatterns
            has_antipatterns = True

            model = r.get("model", "NA")
            prompt = r.get("prompt", "NA")
            detected_str = ", ".join(sorted(detected))
            penalty = metrics.get("antipattern_penalty", "NA")

            lines.append(f"| ({model}) {prompt} | {detected_str} | {penalty} |")

        except Exception:
            lines.append("| NA | NA | NA |")

    if not has_antipatterns:
        lines.append("| NA | NA | No antipatterns detected |")

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
    analyzer = SQLComplexityAnalyzer()  

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

                    engine = result.get("engine") # Note-a: execution success decided HERE
                    metrics = result.get("metrics") or {}

                    # Append metrics from SQLComplexityAnalyzer
                    analysis = analyzer.analyze(sql)

                    metrics.update(analysis.get("runtime", {})) # Runtime
                    features = analysis.get("features", {})     # Features
                    metrics.update(features)
                    for k in ["actual_operator_count", "actual_plan_depth"]:
                        if k in metrics:  # Move actual_* into features 
                            features[k] = metrics.pop(k)
                    metrics.update(analysis.get("antipatterns", {})) # Antipatterns
                    metrics["antipattern_penalty"] = analysis.get("antipattern_penalty") 

                    exec_time = metrics.get("execution_time_avg")
                    complexity = analysis.get("features", {}).get("complexity_score")

                    if exec_time is not None and complexity and complexity > 0:
                        metrics["efficiency"] = exec_time / complexity
                    else:
                        metrics["efficiency"] = None

                    data_preview = None
                    if result and isinstance(result.get("data"), pd.DataFrame):
                        df = result["data"]
                        data_preview = df.head(5).to_dict()

                    if print_results: # Note-a: display AFTER success is locked in
                        try:
                            runner.display_result_head(result, model, prompt_label)
                            runner.display_metrics(result)
                        except Exception as display_error:
                            print(f"(Display Error - ignored): {display_error}")

                engine = result.get("engine") if result else None

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

                if 'run_status' in locals() and run_status == "success":
                    status = "run_all_queries error"
                    error_mssg = str(e)
                
                else:
                    status = run_status
                    old_error = result.get("error")
                    error_mssg = f"{old_error}\n{str(e)}"
            
            results_log.append({"question": question, "model": model,  "prompt": prompt_label, "status": status,
                                "engine": engine,  "metrics": metrics,"data_preview": data_preview, "error": error_mssg})     


    return results_log

def add_normalized_efficiency(results_log):
    """Compute normalized efficiency across a results_log.
    Adds 'normed_efficiency' in each item's metrics dict.
    """
    # collect all valid efficiencies
    efficiencies = [
        r.get("metrics", {}).get("efficiency")
        for r in results_log
        if r.get("metrics", {}).get("efficiency") is not None
    ]

    if not efficiencies:
        return  # nothing to normalize

    min_eff = min(efficiencies)
    max_eff = max(efficiencies)

    for r in results_log:
        metrics = r.get("metrics", {})
        eff = metrics.get("efficiency")

        if eff is None or max_eff == min_eff:
            metrics["normed_efficiency"] = None
        else:
            metrics["normed_efficiency"] = (eff - min_eff) / (max_eff - min_eff)

if __name__ == "__main__":
    question = "top_repos_question" # "Find repos with most python files."

    if BQ_ONLINE:
        runner = BigQueryRunner()
    else:
        runner = DuckDBRunner(mode="dHF_load")

    results_log = run_all_queries(question=question, runner=runner, print_results=True)
    add_normalized_efficiency(results_log)

    save_results_report(results_log, question, save_to_json=True, sort_by="normed_efficiency")