# Query Benchmark Report

**Total Runs:** 7

**Engine:**     duckdb

**Question:**   top_repos_question

## Metrics

| Model | Prompt | Status | antipattern_penalty | efficiency | execution_time_avg | execution_time_max | execution_time_min | normed_efficiency | total_operator_time | total_rows_processed | antipattern_penalty |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen2.5-3B-Instruct | chat_style_prompt | success | NA | 0.0020 | 0.0148 | 0.0204 | 0.0101 | 0.0000 | 0 | 0 | NA |
| ChatGPT-GPT-5.3 | cot_style_prompt | success | NA | 0.0021 | 0.0161 | 0.0167 | 0.0151 | 0.0242 | 0 | 0 | NA |
| Qwen2.5-3B-Instruct | cot_style_prompt | success | NA | 0.0022 | 0.0162 | 0.0196 | 0.0108 | 0.0252 | 0 | 0 | NA |
| ChatGPT-GPT-5.3 | chat_style_prompt | success | NA | 0.0025 | 0.0186 | 0.0196 | 0.0166 | 0.0713 | 0 | 0 | NA |
| Placeholder | basic_sql_prompt | success | NA | 0.0058 | 0.0145 | 0.0182 | 0.0074 | 0.5382 | 0 | 0 | NA |
| ChatGPT-GPT-5.3 | basic_sql_prompt | success | NA | 0.0080 | 0.0160 | 0.0190 | 0.0130 | 0.8510 | 0 | 0 | NA |
| Qwen2.5-3B-Instruct | basic_sql_prompt | success | NA | 0.0091 | 0.0181 | 0.0201 | 0.0170 | 1.0000 | 0 | 0 | NA |

## Data Preview

| Model | Prompt | Data Preview |
| --- | --- | --- |
| Qwen2.5-3B-Instruct | chat_style_prompt | {'repo_name': {0: 'mjirik/imcut', 1: 'astroduff/commah', 2: 'qubell/contrib-python-qubell-client', 3: 'kaste/mockito-python', 4: 'davidblaisonneau-orange/foreman'}, 'total_functions': {0: 35, 1: 19, 2 |
| ChatGPT-GPT-5.3 | cot_style_prompt | {'repo_name': {0: 'mjirik/imcut', 1: 'astroduff/commah', 2: 'qubell/contrib-python-qubell-client', 3: 'davidblaisonneau-orange/foreman', 4: 'kaste/mockito-python'}, 'total_functions': {0: 35, 1: 19, 2 |
| Qwen2.5-3B-Instruct | cot_style_prompt | {'repo_name': {0: 'mjirik/imcut', 1: 'astroduff/commah', 2: 'qubell/contrib-python-qubell-client', 3: 'kaste/mockito-python', 4: 'davidblaisonneau-orange/foreman'}, 'total_functions': {0: 35, 1: 19, 2 |
| ChatGPT-GPT-5.3 | chat_style_prompt | {'repo_name': {0: 'mjirik/imcut', 1: 'astroduff/commah', 2: 'qubell/contrib-python-qubell-client', 3: 'kaste/mockito-python', 4: 'davidblaisonneau-orange/foreman'}, 'total_functions': {0: 35, 1: 19, 2 |
| Placeholder | basic_sql_prompt | {'repo_name': {0: 'mjirik/imcut', 1: 'astroduff/commah', 2: 'qubell/contrib-python-qubell-client', 3: 'kaste/mockito-python', 4: 'davidblaisonneau-orange/foreman'}, 'count': {0: 35, 1: 19, 2: 16, 3: 1 |
| ChatGPT-GPT-5.3 | basic_sql_prompt | {'repo_name': {0: 'mjirik/imcut', 1: 'astroduff/commah', 2: 'qubell/contrib-python-qubell-client', 3: 'kaste/mockito-python', 4: 'davidblaisonneau-orange/foreman'}, 'num_files': {0: 35, 1: 19, 2: 16,  |
| Qwen2.5-3B-Instruct | basic_sql_prompt | {'repo_name': {0: 'mjirik/imcut', 1: 'astroduff/commah', 2: 'qubell/contrib-python-qubell-client', 3: 'kaste/mockito-python', 4: 'davidblaisonneau-orange/foreman'}, 'num_files': {0: 35, 1: 19, 2: 16,  |

## Features

| Model | Prompt | actual_operator_count | actual_plan_depth | estimated_operator_count | estimated_plan_depth | nesting_depth | num_conditions | num_ctes | num_group_by | num_joins | num_subqueries | num_window_functions | sql_token_count | complexity_score | complexity_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen2.5-3B-Instruct | chat_style_prompt | NA | NA | 5 | 2 | 2 | 1 | 1 | 1 | 0 | 1 | 0 | 53 | 7.5000 | 7.5000 |
| ChatGPT-GPT-5.3 | cot_style_prompt | NA | NA | 5 | 2 | 2 | 1 | 1 | 1 | 0 | 1 | 0 | 53 | 7.5000 | 7.5000 |
| Qwen2.5-3B-Instruct | cot_style_prompt | NA | NA | 5 | 2 | 2 | 1 | 1 | 1 | 0 | 1 | 0 | 53 | 7.5000 | 7.5000 |
| ChatGPT-GPT-5.3 | chat_style_prompt | NA | NA | 5 | 2 | 2 | 1 | 1 | 1 | 0 | 1 | 0 | 53 | 7.5000 | 7.5000 |
| Placeholder | basic_sql_prompt | NA | NA | 4 | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 25 | 2.5000 | 2.5000 |
| ChatGPT-GPT-5.3 | basic_sql_prompt | NA | NA | 3 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 20 | 2.0000 | 2.0000 |
| Qwen2.5-3B-Instruct | basic_sql_prompt | NA | NA | 3 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 20 | 2.0000 | 2.0000 |

## Antipatterns

| (Model) Prompt | Antipatterns Detected | Penalty |
| --- | --- | --- |
| (Qwen2.5-3B-Instruct) chat_style_prompt | has_subquery_no_join | None |
| (ChatGPT-GPT-5.3) cot_style_prompt | has_subquery_no_join | None |
| (Qwen2.5-3B-Instruct) cot_style_prompt | has_subquery_no_join | None |
| (ChatGPT-GPT-5.3) chat_style_prompt | has_subquery_no_join | None |

## Errors

| (Model) Prompt | Status | Error Message |
| --- | --- | --- |
| NA | NA | No errors |