try:
    import json
    import boto3
    import os
    import csv
    import time
    from datetime import datetime
    from dotenv import load_dotenv

    load_dotenv(".env")
except Exception as e:
    pass

def run():
    s3_client = boto3.client(
        's3',
         aws_access_key_id = os.getenv("DEV_AWS_ACCESS_KEY"),
         aws_secret_access_key = os.getenv("DEV_AWS_SECRET_KEY")
    )

    with open("C:/Users/dat/MXH/GoodReads_100k_books.csv", newline='', encoding="utf8") as f:
        reader = csv.reader(f)
        columns = [column.replace("\ufeff", "") for column in next(reader)] # first row (header)
        columns.append("id") # add id
        columns.append("ts")  # add timestamp

        i = 1
        # Upload all file csv include 100k record:

        for row in reader:
        # for row in list(reader)[:200]: # just upload 200 record
            print("upload file: ", i, end="") # print info

            json_file_name = f'data/row_{i}.json'
            row.append(str(i))
            row.append(datetime.now().isoformat().__str__(),)
            json_data = json.dumps(dict(zip(columns, tuple(row))))

            # s3_client.put_object(Body=json_data.encode('UTF-8'), Bucket='dataset-books', Key=json_file_name)
            s3_client.put_object(Body=json_data.encode('UTF-8'), Bucket='test-adding', Key=json_file_name)

            i += 1
            print("\r", end="") # clear last output

if __name__ == "__main__":
    run()