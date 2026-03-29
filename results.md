# Prompts
## Basic SQL prompt
'''
Act as a BigQuery SQL Expert.
Write a query for the `bigquery-public-data.github_repos.sample_repos` table.
I want to see the repo_name and watch_count for the top 10 most watched repos.
'''

## Chain-of-Thought styled Prompt
```
**Context**: I am analyzing the 'bigquery-public-data.github_repos' dataset.
**Objective**: Identify 'Hot but Fragile' repositories.
**Logic**:
1. Filter the 'commits' table for repos with > 10,000 total commits.
2. Filter for repos that have fewer than 5 unique contributors in the last 12 months (use committer.time_sec).
3. Join with the 'languages' table to show the primary language.

Output **Constraints**:
- Use Standard SQL.
- Handle the nested 'committer' record correctly.
- Limit to top 20 by commit count.
```

## Chat-style Prompt
```
**role: "system"**
**content**: 
You are an expert BigQuery analyst specializing in the bigquery-public-data.github_repos dataset. 
Your job is to reason step-by-step about repository activity, contributors, commit history, and language metadata. 
When answering, first explain your reasoning in natural language, then produce clean, correct Standard SQL.
```

```
**role": "user"**
**content**: 
Identify 'Hot but Fragile' open-source repositories. A repository is 'Hot but Fragile' if:"
    1. It has more than 10,000 total commits."
    "2. It has fewer than 5 unique contributors in the last 12 months."
    "3. It has a primary language listed in the languages table."

- Use the bigquery-public-data.github_repos.commits and bigquery-public-data.github_repos.languages tables. 
- Handle the nested committer record correctly. 
- Limit to the top 20 by commit count. 
- "Explain your reasoning before writing SQL.
```

# Results
## Qwen/Qwen2.5-3B-Instruct model
3-billion-parameter causal language model optimized for instruction-following tasks. 
In this setup, it is loaded in 4-bit quantized form using bitsandbytes with nf4 quantization, double quantization enabled, and float16 compute. 
All weights are placed on the CPU (``device_map={"": "cpu"}``) to avoid GPU compatibility issues. 

Reasons:
- drastically reduces memory usage while maintaining reasonable inference quality, suitable for devices with limited GPU VRAM (~8.5 GB) 
- at the cost of slower CPU-based execution.

