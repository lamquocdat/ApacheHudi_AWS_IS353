import json

try:
    import boto3
    import os
    from datetime import datetime
    from dotenv import load_dotenv

    load_dotenv(".env")
except Exception as e:
    pass

glue = boto3.client(
    "glue",
    aws_access_key_id=os.getenv("DEV_AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("DEV_AWS_SECRET_KEY"),
    region_name=os.getenv("DEV_AWS_REGION_NAME"),
)

job_name = 'delete_test'
glue_database = 'hudidb'
glue_table_name = 'dataset'
hoodies_pre_key = 'ts'
hoodies_record_key = 'id'
source_s3_path = 's3://test-adding/data/' # s3://dataset-books/data/
target_s3_path = 's3://test-adding/hudi/'
deletes = [
    ('bookformat', ''),
    ('genre', '')
]

payloads = [
    {
        'JOB_NAME': job_name,
        'GLUE_DATABASE': glue_database,
        'GLUE_TABLE_NAME': glue_table_name,
        'HUDI_PRECOMB_KEY': hoodies_pre_key, # timestamp
        'HUDI_RECORD_KEY': hoodies_record_key, # primary key
        'SOURCE_S3_PATH': source_s3_path, # data source
        'TARGET_S3_PATH': target_s3_path,
        'DELETES': deletes
    }
]

for payload in payloads:
    job_name = 'Hudi_delete_job' # Hudi_delete_job.py

    fire_payload = {}
    for key, value in payload.items():
        if key == 'DELETES':
            fire_payload[f"--{key}"] = json.dumps(value)
        else:
            fire_payload[f"--{key}"] = value

    response = glue.start_job_run(
        JobName=job_name,
        Arguments=fire_payload
    )

    print(response)