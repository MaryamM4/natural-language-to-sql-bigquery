# Query Benchmark Report

**Total Runs:** 7

**Engine:**     duckdb

**Question:**   top_repos_question

## Metrics

| Model | Prompt | Status | efficiency | execution_time_avg | execution_time_max | execution_time_min | normed_efficiency | total_operator_time | total_rows_processed | antipattern_penalty |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen2.5-3B-Instruct | chat_style_prompt | success | 0.0021 | 0.0159 | 0.0201 | 0.0138 | 0.0000 | 0 | 0 | 0.0000 |
| ChatGPT-GPT-5.3 | cot_style_prompt | success | 0.0023 | 0.0170 | 0.0184 | 0.0154 | 0.0223 | 0 | 0 | 0.0000 |
| ChatGPT-GPT-5.3 | chat_style_prompt | success | 0.0023 | 0.0172 | 0.0213 | 0.0122 | 0.0264 | 0 | 0 | 0.0000 |
| Qwen2.5-3B-Instruct | cot_style_prompt | success | 0.0023 | 0.0174 | 0.0191 | 0.0152 | 0.0299 | 0 | 0 | 0.0000 |
| Placeholder | basic_sql_prompt | success | 0.0056 | 0.0141 | 0.0168 | 0.0067 | 0.5477 | 0 | 0 | 0.0000 |
| ChatGPT-GPT-5.3 | basic_sql_prompt | success | 0.0073 | 0.0145 | 0.0156 | 0.0114 | 0.8035 | 0 | 0 | 0.0000 |
| Qwen2.5-3B-Instruct | basic_sql_prompt | success | 0.0085 | 0.0171 | 0.0182 | 0.0161 | 1.0000 | 0 | 0 | 0.0000 |

## Data Preview

| Model | Prompt | Data Preview |
| --- | --- | --- |
| Qwen2.5-3B-Instruct | chat_style_prompt | {'repo_name': {0: 'mjirik/imcut', 1: 'astroduff/commah', 2: 'qubell/contrib-python-qubell-client', 3: 'kaste/mockito-python', 4: 'davidblaisonneau-orange/foreman'}, 'total_functions': {0: 35, 1: 19, 2 |
| ChatGPT-GPT-5.3 | cot_style_prompt | {'repo_name': {0: 'mjirik/imcut', 1: 'astroduff/commah', 2: 'qubell/contrib-python-qubell-client', 3: 'davidblaisonneau-orange/foreman', 4: 'kaste/mockito-python'}, 'total_functions': {0: 35, 1: 19, 2 |
| ChatGPT-GPT-5.3 | chat_style_prompt | {'repo_name': {0: 'mjirik/imcut', 1: 'astroduff/commah', 2: 'qubell/contrib-python-qubell-client', 3: 'kaste/mockito-python', 4: 'davidblaisonneau-orange/foreman'}, 'total_functions': {0: 35, 1: 19, 2 |
| Qwen2.5-3B-Instruct | cot_style_prompt | {'repo_name': {0: 'mjirik/imcut', 1: 'astroduff/commah', 2: 'qubell/contrib-python-qubell-client', 3: 'kaste/mockito-python', 4: 'davidblaisonneau-orange/foreman'}, 'total_functions': {0: 35, 1: 19, 2 |
| Placeholder | basic_sql_prompt | {'repo_name': {0: 'mjirik/imcut', 1: 'astroduff/commah', 2: 'qubell/contrib-python-qubell-client', 3: 'kaste/mockito-python', 4: 'davidblaisonneau-orange/foreman'}, 'count': {0: 35, 1: 19, 2: 16, 3: 1 |
| ChatGPT-GPT-5.3 | basic_sql_prompt | {'repo_name': {0: 'mjirik/imcut', 1: 'astroduff/commah', 2: 'qubell/contrib-python-qubell-client', 3: 'davidblaisonneau-orange/foreman', 4: 'kaste/mockito-python'}, 'num_files': {0: 35, 1: 19, 2: 16,  |
| Qwen2.5-3B-Instruct | basic_sql_prompt | {'repo_name': {0: 'mjirik/imcut', 1: 'astroduff/commah', 2: 'qubell/contrib-python-qubell-client', 3: 'kaste/mockito-python', 4: 'davidblaisonneau-orange/foreman'}, 'num_files': {0: 35, 1: 19, 2: 16,  |

## Features

| Model | Prompt | actual_operator_count | actual_plan_depth | estimated_operator_count | estimated_plan_depth | nesting_depth | num_conditions | num_ctes | num_group_by | num_joins | num_subqueries | num_window_functions | sql_token_count | complexity_score | complexity_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen2.5-3B-Instruct | chat_style_prompt | NA | NA | 5 | 2 | 2 | 1 | 1 | 1 | 0 | 1 | 0 | 53 | NA | NA |
| ChatGPT-GPT-5.3 | cot_style_prompt | NA | NA | 5 | 2 | 2 | 1 | 1 | 1 | 0 | 1 | 0 | 53 | NA | NA |
| ChatGPT-GPT-5.3 | chat_style_prompt | NA | NA | 5 | 2 | 2 | 1 | 1 | 1 | 0 | 1 | 0 | 53 | NA | NA |
| Qwen2.5-3B-Instruct | cot_style_prompt | NA | NA | 5 | 2 | 2 | 1 | 1 | 1 | 0 | 1 | 0 | 53 | NA | NA |
| Placeholder | basic_sql_prompt | NA | NA | 4 | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 25 | NA | NA |
| ChatGPT-GPT-5.3 | basic_sql_prompt | NA | NA | 3 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 20 | NA | NA |
| Qwen2.5-3B-Instruct | basic_sql_prompt | NA | NA | 3 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 20 | NA | NA |

## Antipatterns

| (Model) Prompt | Antipatterns Detected | Penalty |
| --- | --- | --- |
| (Qwen2.5-3B-Instruct) chat_style_prompt | has_subquery_no_join | 0.0 |
| (ChatGPT-GPT-5.3) cot_style_prompt | has_subquery_no_join | 0.0 |
| (ChatGPT-GPT-5.3) chat_style_prompt | has_subquery_no_join | 0.0 |
| (Qwen2.5-3B-Instruct) cot_style_prompt | has_subquery_no_join | 0.0 |

## Errors

| (Model) Prompt | Status | Error Message |
| --- | --- | --- |
| NA | NA | No errors |