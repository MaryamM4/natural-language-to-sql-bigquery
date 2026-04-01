# natural-language-to-sql-bigquery
Python script that takes a natural language question, asks an AI for the corresponding SQL, and then executes that SQL against Google BigQuery.

## BigQuery Prerequisites
- Python environment (Cloud Shell or local).
- google-cloud-bigquery library installed: ``pip install google-cloud-bigquery pandas db-dtypes``
- GCP Credentials configured: ``gcloud auth application-default login``
- Set project ID: ``gcloud config set project PROJECT_ID``
    Grab project ID from [Google Cloud Console](https://console.cloud.google.com/welcome?authuser=1&organizationId=657476903663)

Tests require additional libraries:
``pip install -U transformers accelerate bitsandbytes sentencepiece safetensors``

## Cloud Computing Lab Requirements
- Code: You must write functional Python code that uses the BigQuery Client Library.
- Validation: The script must successfully retrieve data without errors.

## Results
