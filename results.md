# Query Benchmark Report

**Total Runs:** 7

**Engine:**     duckdb

**Question:**   top_repos_question

## Metrics

| Model | Prompt | Status | efficiency | execution_time_avg | execution_time_max | execution_time_min | normed_efficiency | total_operator_time | total_rows_processed | antipattern_penalty |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ChatGPT-GPT-5.3 | cot_style_prompt | success | 0.0019 | 0.0145 | 0.0162 | 0.0107 | 0.0000 | 0 | 0 | 0.0000 |
| Qwen2.5-3B-Instruct | chat_style_prompt | success | 0.0021 | 0.0157 | 0.0182 | 0.0135 | 0.0274 | 0 | 0 | 0.0000 |
| Qwen2.5-3B-Instruct | cot_style_prompt | success | 0.0021 | 0.0159 | 0.0174 | 0.0141 | 0.0320 | 0 | 0 | 0.0000 |
| ChatGPT-GPT-5.3 | chat_style_prompt | success | 0.0023 | 0.0173 | 0.0207 | 0.0161 | 0.0671 | 0 | 0 | 0.0000 |
| Placeholder | basic_sql_prompt | success | 0.0054 | 0.0136 | 0.0170 | 0.0088 | 0.6251 | 0 | 0 | 0.0000 |
| ChatGPT-GPT-5.3 | basic_sql_prompt | success | 0.0070 | 0.0139 | 0.0161 | 0.0093 | 0.8946 | 0 | 0 | 0.0000 |
| Qwen2.5-3B-Instruct | basic_sql_prompt | success | 0.0075 | 0.0151 | 0.0173 | 0.0140 | 1.0000 | 0 | 0 | 0.0000 |

## Data Preview

| Model | Prompt | Data Preview |
| --- | --- | --- |
| ChatGPT-GPT-5.3 | cot_style_prompt | {'repo_name': {0: 'mjirik/imcut', 1: 'astroduff/commah', 2: 'qubell/contrib-python-qubell-client', 3: 'davidblaisonneau-orange/foreman', 4: 'kaste/mockito-python'}, 'total_functions': {0: 35, 1: 19, 2 |
| Qwen2.5-3B-Instruct | chat_style_prompt | {'repo_name': {0: 'mjirik/imcut', 1: 'astroduff/commah', 2: 'qubell/contrib-python-qubell-client', 3: 'davidblaisonneau-orange/foreman', 4: 'kaste/mockito-python'}, 'total_functions': {0: 35, 1: 19, 2 |
| Qwen2.5-3B-Instruct | cot_style_prompt | {'repo_name': {0: 'mjirik/imcut', 1: 'astroduff/commah', 2: 'qubell/contrib-python-qubell-client', 3: 'kaste/mockito-python', 4: 'davidblaisonneau-orange/foreman'}, 'total_functions': {0: 35, 1: 19, 2 |
| ChatGPT-GPT-5.3 | chat_style_prompt | {'repo_name': {0: 'mjirik/imcut', 1: 'astroduff/commah', 2: 'qubell/contrib-python-qubell-client', 3: 'kaste/mockito-python', 4: 'davidblaisonneau-orange/foreman'}, 'total_functions': {0: 35, 1: 19, 2 |
| Placeholder | basic_sql_prompt | {'repo_name': {0: 'mjirik/imcut', 1: 'astroduff/commah', 2: 'qubell/contrib-python-qubell-client', 3: 'kaste/mockito-python', 4: 'davidblaisonneau-orange/foreman'}, 'count': {0: 35, 1: 19, 2: 16, 3: 1 |
| ChatGPT-GPT-5.3 | basic_sql_prompt | {'repo_name': {0: 'mjirik/imcut', 1: 'astroduff/commah', 2: 'qubell/contrib-python-qubell-client', 3: 'kaste/mockito-python', 4: 'davidblaisonneau-orange/foreman'}, 'num_files': {0: 35, 1: 19, 2: 16,  |
| Qwen2.5-3B-Instruct | basic_sql_prompt | {'repo_name': {0: 'mjirik/imcut', 1: 'astroduff/commah', 2: 'qubell/contrib-python-qubell-client', 3: 'davidblaisonneau-orange/foreman', 4: 'kaste/mockito-python'}, 'num_files': {0: 35, 1: 19, 2: 16,  |

## Features

| Model | Prompt | actual_operator_count | actual_plan_depth | estimated_operator_count | estimated_plan_depth | nesting_depth | num_conditions | num_ctes | num_group_by | num_joins | num_subqueries | num_window_functions | sql_token_count | complexity_score | complexity_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ChatGPT-GPT-5.3 | cot_style_prompt | NA | NA | 5 | 2 | 2 | 1 | 1 | 1 | 0 | 1 | 0 | 53 | NA | NA |
| Qwen2.5-3B-Instruct | chat_style_prompt | NA | NA | 5 | 2 | 2 | 1 | 1 | 1 | 0 | 1 | 0 | 53 | NA | NA |
| Qwen2.5-3B-Instruct | cot_style_prompt | NA | NA | 5 | 2 | 2 | 1 | 1 | 1 | 0 | 1 | 0 | 53 | NA | NA |
| ChatGPT-GPT-5.3 | chat_style_prompt | NA | NA | 5 | 2 | 2 | 1 | 1 | 1 | 0 | 1 | 0 | 53 | NA | NA |
| Placeholder | basic_sql_prompt | NA | NA | 4 | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 25 | NA | NA |
| ChatGPT-GPT-5.3 | basic_sql_prompt | NA | NA | 3 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 20 | NA | NA |
| Qwen2.5-3B-Instruct | basic_sql_prompt | NA | NA | 3 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 20 | NA | NA |

## Antipatterns

| (Model) Prompt | Antipatterns Detected | Penalty |
| --- | --- | --- |
| (ChatGPT-GPT-5.3) cot_style_prompt | has_subquery_no_join | 0.0 |
| (Qwen2.5-3B-Instruct) chat_style_prompt | has_subquery_no_join | 0.0 |
| (Qwen2.5-3B-Instruct) cot_style_prompt | has_subquery_no_join | 0.0 |
| (ChatGPT-GPT-5.3) chat_style_prompt | has_subquery_no_join | 0.0 |

## Errors

| (Model) Prompt | Status | Error Message |
| --- | --- | --- |
| NA | NA | No errors |