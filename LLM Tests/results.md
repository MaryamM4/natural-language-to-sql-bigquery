# Prompts
## Basic SQL prompt
'''
Act as a BigQuery SQL Expert.
Write a query for the `bigquery-public-data.github_repos.sample_repos` table.
I want to see the repo_name and watch_count for the top 10 most watched repos.
'''

## Chain-of-Thought styled Prompt
```
Context: I am analyzing the 'bigquery-public-data.github_repos' dataset.
Objective: Identify 'Hot but Fragile' repositories.
Logic:
1. Filter the 'commits' table for repos with > 10,000 total commits.
2. Filter for repos that have fewer than 5 unique contributors in the last 12 months (use committer.time_sec).
3. Join with the 'languages' table to show the primary language.

Output Constraints:
- Use Standard SQL.
- Handle the nested 'committer' record correctly.
- Limit to top 20 by commit count.
```

## Chat-style Prompt
**role: "system"**
**content:**: 
```
You are an expert BigQuery analyst specializing in the bigquery-public-data.github_repos dataset. 
Your job is to reason step-by-step about repository activity, contributors, commit history, and language metadata. 
When answering, first explain your reasoning in natural language, then produce clean, correct Standard SQL.
```

**role": "user"**
**content:**: 
```
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

Note: It's VERY slow (test lasted 53 mins and counting)
- Running even a 3B parameter model entirely on CPU is extremely slow.
- 4-bit quantization reduces RAM usage, but does not speed up CPU inference significantly
- Sampling parameter: Sampling adds computation compared to greedy decoding

### Basic:
Act as a BigQuery SQL Expert.
Write a query for the `bigquery-public-data.github_repos.sample_repos` table.
I want to see the repo_name and watch_count for the top 10 most watched repos.

Sure, you can use the following SQL query to retrieve the top 10 most watched repositories along with their `watch_count` from the `sample_repos` table:
```sql
SELECT 
    repo_name,
    watch_count
FROM 
    bigquery-public-data.github_repos.sample_repos
ORDER BY 
    watch_count DESC
LIMIT 10;
```

This query will sort the repositories by their `watch_count` in descending order (so the highest watched ones are at the top) and then limit the results to the top 10. Make sure that the `watch_count` column exists in your table and is correctly named. If it's different, adjust the column name accordingly.

### Chain-of-Thought:
Context: I am analyzing the 'bigquery-public-data.github_repos' dataset.
Objective: Identify 'Hot but Fragile' repositories.

Logic:
1. Filter the 'commits' table for repos with > 10,000 total commits.
2. Filter for repos that have fewer than 5 unique contributors in the last 12 months (use committer.time_sec).
3. Join with the 'languages' table to show the primary language.

Output Constraints:
- Use Standard SQL.
- Handle the nested 'committer' record correctly.
- Limit to top 20 by commit count.

```sql
SELECT 
    l.primary_language AS primary_language,
    c.repos_name AS repository_name,
    COUNT(*) AS commit_count
FROM 
    `bigquery-public-data.github_repos.commits` AS c
JOIN 
    `bigquery-public-data.github_repos.languages` AS l
ON 
    c.repos_name = l.repos_name
WHERE 
    c.total_commits > 10000
    AND c.committer_time_sec > DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR)
GROUP BY 
    l.primary_language, c.repos_name
HAVING 
    COUNT(DISTINCT c.committer_id) < 5
ORDER BY 
    commit_count DESC
LIMIT 20;
```

This query filters and joins the necessary tables to identify repositories that are both 'hot' (with many commits) and 'fragile' (with few unique contributors). It then limits the output to the top 20 by commit count, ensuring we focus on the most active and potentially unstable repositories. 

## Chat-style Prompt:
```sql
SELECT 
    l.primary_language AS primary_language,
    c.repos_name AS repository_name,
    COUNT(*) AS commit_count
FROM 
    `bigquery-public-data.github_repos.commits` AS c
JOIN 
    `bigquery-public-data.github_repos.languages` AS l
ON 
    c.repos_name = l.repos_name
WHERE 
    c.total_commits > 10000
    AND c.committer_time_sec > DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR)
GROUP BY 
    l.primary_language, c.repos_name
HAVING 
    COUNT(DISTINCT c.committer_id) < 5
ORDER BY 
    commit_count DESC
LIMIT 20;
```

## ChatGPT/GPT-5.3
### Basic:
Here’s the BigQuery SQL query to get the **top 10 most watched repositories** from the `bigquery-public-data.github_repos.sample_repos` table:
```sql
SELECT
  repo_name,
  watch_count
FROM
  `bigquery-public-data.github_repos.sample_repos`
ORDER BY
  watch_count DESC
LIMIT 10;
```

**Explanation:**
* `repo_name` and `watch_count` are selected as requested.
* Results are sorted in descending order by `watch_count`.
* `LIMIT 10` ensures only the top 10 most watched repositories are returned.

### Chain-of-Thought:
Here’s a **Standard SQL** query for BigQuery that follows your logic and correctly handles the nested `committer` field:

```sql
-- Standard SQL
WITH repo_commit_counts AS (
  SELECT
    repo_name,
    COUNT(1) AS total_commits
  FROM
    `bigquery-public-data.github_repos.commits`
  GROUP BY
    repo_name
  HAVING
    total_commits > 10000
),

recent_contributors AS (
  SELECT
    repo_name,
    COUNT(DISTINCT committer.email) AS contributors_last_12mo
  FROM
    `bigquery-public-data.github_repos.commits`
  WHERE
    committer.time_sec >= UNIX_SECONDS(TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 12 MONTH))
    AND committer.email IS NOT NULL
  GROUP BY
    repo_name
  HAVING
    contributors_last_12mo < 5
),

primary_languages AS (
  SELECT
    repo_name,
    language AS primary_language
  FROM (
    SELECT
      repo_name,
      language,
      bytes,
      ROW_NUMBER() OVER (PARTITION BY repo_name ORDER BY bytes DESC) AS rn
    FROM
      `bigquery-public-data.github_repos.languages`
  )
  WHERE rn = 1
)

SELECT
  r.repo_name,
  r.total_commits,
  c.contributors_last_12mo,
  l.primary_language
FROM
  repo_commit_counts r
JOIN
  recent_contributors c
ON
  r.repo_name = c.repo_name
LEFT JOIN
  primary_languages l
ON
  r.repo_name = l.repo_name
ORDER BY
  r.total_commits DESC
LIMIT 20;
```

***Key Points**:
* **Commit threshold (>10,000):** handled in `repo_commit_counts`.
* **Recent contributor filter (<5 in last 12 months):**
  * Uses `committer.time_sec` (UNIX timestamp).
  * Counts distinct `committer.email`.
* **Nested field handling:** `committer.email` and `committer.time_sec` are accessed directly from the STRUCT.
* **Primary language:** selected via `ROW_NUMBER()` over `bytes`.
* **Final output:** top 20 repos by total commits that are “hot but fragile.”

If you want, I can extend this to include additional signals (e.g., issue activity or star growth) to refine the “fragility” definition.

## Chat-style Prompt:
Here’s the reasoning at a high level (without exposing unnecessary step-by-step detail):

We’re looking for repositories that are very active historically (“hot”) but currently maintained by very few people (“fragile”).

* “Hot” is captured by **total commit count > 10,000** from the `commits` table.
* “Fragile” is captured by **fewer than 5 distinct contributors in the last 12 months**, which requires:
  * Filtering commits to the past year using the commit timestamp.
  * Counting distinct contributors via the nested `committer` field (typically `committer.email` or `committer.name`).
* We also ensure the repo has a **primary language**, which we approximate by requiring a match in the `languages` table.
* Finally, we sort by total commits and return the top 20.

✅ **BigQuery Standard SQL:**
```sql
WITH all_time_commits AS (
  SELECT
    repo_name,
    COUNT(1) AS total_commits
  FROM `bigquery-public-data.github_repos.commits`
  GROUP BY repo_name
),

recent_contributors AS (
  SELECT
    repo_name,
    COUNT(DISTINCT committer.email) AS contributors_last_12mo
  FROM `bigquery-public-data.github_repos.commits`
  WHERE
    committer.email IS NOT NULL
    AND DATE(committer.date) >= DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH)
  GROUP BY repo_name
),

repos_with_language AS (
  SELECT DISTINCT
    repo_name
  FROM `bigquery-public-data.github_repos.languages`
)

SELECT
  c.repo_name,
  c.total_commits,
  rc.contributors_last_12mo
FROM all_time_commits c
JOIN recent_contributors rc
  ON c.repo_name = rc.repo_name
JOIN repos_with_language l
  ON c.repo_name = l.repo_name
WHERE
  c.total_commits > 10000
  AND rc.contributors_last_12mo < 5
ORDER BY
  c.total_commits DESC
LIMIT 20;
```

**Notes:**
* `committer.email` is used as a proxy for unique contributors (more reliable than names).
* The `languages` table doesn’t explicitly label a “primary” language, so we treat presence in that table as satisfying the requirement.
* If you want a stricter definition of “primary language” (e.g., highest byte count), we could refine that further.
