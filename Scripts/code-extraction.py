import os
from datasets import load_dataset
from dotenv import load_dotenv
import boto3
from smart_open import open

load_dotenv()



session = boto3.Session(
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"])
s3 = session.client("s3")


# from file ids download the content of the files
def download_contents(files):
    for file in files:
        s3_url = f"s3://softwareheritage/content/{file['blob_id']}"
        with open(s3_url, "rb", compression=".gz", transport_params={"client": s3}) as fin:
            file['content'] = fin.read().decode(file['src_encoding'])
    
    return {"files": files}

# load the ids of the file
ds = load_dataset("bigcode/the-stack-v2-train-smol-ids", streaming=True, split="train")

# map the rows ( each rows consists of files ) to the file ids of the repo
ds = ds.map( lambda row: download_contents(row['files']))


# print the files
for row in ds:
    for file in row['files']:
        print(file['content'])
    break