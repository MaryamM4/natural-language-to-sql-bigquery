# Query Benchmark Report

**Total Runs:** 7

**Engine:**     duckdb
**Question:**   top_repos_question

## Metrics

| Model | Prompt | Status | execution_time_avg | execution_time_max | execution_time_min |
| --- | --- | --- | --- | --- | --- |
| ChatGPT-GPT-5.3 | basic_sql_prompt | success | 0.0008 | 0.0010 | 0.0007 |
| Qwen2.5-3B-Instruct | basic_sql_prompt | success | 0.0010 | 0.0011 | 0.0008 |
| Placeholder | basic_sql_prompt | success | 0.0016 | 0.0023 | 0.0010 |
| ChatGPT-GPT-5.3 | cot_style_prompt | success | 0.0023 | 0.0026 | 0.0020 |
| Qwen2.5-3B-Instruct | chat_style_prompt | success | 0.0023 | 0.0025 | 0.0022 |
| ChatGPT-GPT-5.3 | chat_style_prompt | success | 0.0024 | 0.0028 | 0.0022 |
| Qwen2.5-3B-Instruct | cot_style_prompt | success | 0.0026 | 0.0033 | 0.0022 |

## Data Preview

| Model | Prompt | Data Preview |
| --- | --- | --- |
| ChatGPT-GPT-5.3 | basic_sql_prompt | {'repo_name': {0: 'mjirik/imcut', 1: 'astroduff/commah', 2: 'qubell/contrib-python-qubell-client', 3: 'davidblaisonneau-orange/foreman', 4: 'kaste/mockito-python'}, 'num_files': {0: 35, 1: 19, 2: 16,  |
| Qwen2.5-3B-Instruct | basic_sql_prompt | {'repo_name': {0: 'mjirik/imcut', 1: 'astroduff/commah', 2: 'qubell/contrib-python-qubell-client', 3: 'davidblaisonneau-orange/foreman', 4: 'kaste/mockito-python'}, 'num_files': {0: 35, 1: 19, 2: 16,  |
| Placeholder | basic_sql_prompt | {'repo_name': {0: 'mjirik/imcut', 1: 'astroduff/commah', 2: 'qubell/contrib-python-qubell-client', 3: 'davidblaisonneau-orange/foreman', 4: 'kaste/mockito-python'}, 'count': {0: 35, 1: 19, 2: 16, 3: 1 |
| ChatGPT-GPT-5.3 | cot_style_prompt | {'repo_name': {0: 'mjirik/imcut', 1: 'astroduff/commah', 2: 'qubell/contrib-python-qubell-client', 3: 'davidblaisonneau-orange/foreman', 4: 'kaste/mockito-python'}, 'total_functions': {0: 35, 1: 19, 2 |
| Qwen2.5-3B-Instruct | chat_style_prompt | {'repo_name': {0: 'mjirik/imcut', 1: 'astroduff/commah', 2: 'qubell/contrib-python-qubell-client', 3: 'davidblaisonneau-orange/foreman', 4: 'kaste/mockito-python'}, 'total_functions': {0: 35, 1: 19, 2 |
| ChatGPT-GPT-5.3 | chat_style_prompt | {'repo_name': {0: 'mjirik/imcut', 1: 'astroduff/commah', 2: 'qubell/contrib-python-qubell-client', 3: 'kaste/mockito-python', 4: 'davidblaisonneau-orange/foreman'}, 'total_functions': {0: 35, 1: 19, 2 |
| Qwen2.5-3B-Instruct | cot_style_prompt | {'repo_name': {0: 'mjirik/imcut', 1: 'astroduff/commah', 2: 'qubell/contrib-python-qubell-client', 3: 'kaste/mockito-python', 4: 'davidblaisonneau-orange/foreman'}, 'total_functions': {0: 35, 1: 19, 2 |

## Errors

| (Model) Prompt | Status | Error Message |
| --- | --- | --- |
| NA | NA | No errors |