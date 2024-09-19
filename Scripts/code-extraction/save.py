import os
from datasets import load_dataset
from smart_open import open
import json
from datetime import datetime
# local imoport
from download import download_contents

output_dir = './new-python-dataset'
MAX_LIMIT = 1000
'''
Directory Meta Data
<START_DIR_METADATA>
{
  "repo_name": "shuishen112/pairwise-rnn",
  "repo_url": "https://github.com/shuishen112/pairwise-rnn",
  "snapshot_id": "2e8d800ef711ed95a3e75a18cac98dc4fb75fe5d",
  "revision_id": "f290baf3afde5e67c5ad0b21244d19cbc14869df",
  "directory_id": "7d88427c34ee31e4d71bc609006d3dfdca92fb39",
  "branch_name": "refs/heads/master",
  "visit_date": "2021-09-04T17:22:29.355846",
  "revision_date": "2018-01-20T10:00:56",
  "committer_date": "2018-01-20T10:00:56",
  "github_id": 106633864,
  "star_events_count": 5,
  "fork_events_count": 0,
  "gha_license_id": null,
  "gha_created_at": null,
  "gha_updated_at": null,
  "gha_pushed_at": null,
  "gha_language": "Python",
  "files": [ <File Meta DATA> ],
  "num_files": 8
}

<END_DIR_METADATA>
'''

'''
File Meta Data

<START_FILE_METADATA>
{
"blob_id": "79802139049c977df9d56776869280cf0baf4d03",
"path": "/README.md",
"content_id": "56d4b7c3dd9756739f6d7bbaaaa758c1f3ecdd47",
"language": "Markdown", 
"length_bytes": 50, 
"detected_licenses": [ "MIT" ], 
"license_type": "permissive", 
"src_encoding": "UTF-8", 
"is_vendor": false, 
"is_generated": false, 
"alphanum_fraction": 0.7200000286102295, 
"alpha_fraction": 0.7200000286102295, 
"num_lines": 4, 
"avg_line_length": 11.5,
"max_line_length": 40
}
<END_FILE_METADATA>

'''




# load the ids of the file
ds = load_dataset("bigcode/the-stack-v2-train-smol-ids", streaming=True, split="train")

# supported files
supported_languages = ['Python']
language_count = {language: 0 for language in supported_languages}

# only keep python files
ds = ds.filter(lambda row: row['gha_language'] in supported_languages)

def serialize_data(row):
    serialized_row = {}
    for key, value in row.items():
        if isinstance(value, datetime):
            serialized_row[key] = value.isoformat()
        else:
            serialized_row[key] = value

    return serialized_row

for i, row in enumerate(ds):
    
    # increase the count
    language_count[row['gha_language']] += 1

    # remove the "files" key from the metadata as individiual file will have it
    content = download_contents(row['files'], supported_languages)

    repo_name = row['repo_name'].replace('/', '_')


    if os.path.exists(f"{output_dir}/{repo_name}.json"):
        print(f"{output_dir}/{repo_name}.json skipped")
        continue
    with open(f"{output_dir}/{repo_name}.json", 'w') as f:
        
        row['files'] = content['files']
        string_data = json.dumps(serialize_data(row))
        f.write(string_data)
    
    if language_count[row['gha_language']] > MAX_LIMIT:
        break












# for teaching aashish only 

# for i, row in enumerate(ds):
#     print(row['gha_language'])
#     # if i == 0 or row['gha_language'] != 'Python':
#     #     continue
#     if i == MAX_LIMIT:
#         break
#     continue
#     # remove the "files" key from the metadata as individiual file will have it
#     files = download_contents(row['files'])['files']

#     # for key, value in row.items():
#     #     print(f"{key}: {type(value)}")
#     with open(f"code.txt", 'a') as f:
#         for file in files:

#             code_content = "<file_sep>\n"+ file['content'] + "<|endoftext|>"
#             # string_data = json.dumps(code_content)
#             f.write(code_content)
    
#     if i == MAX_LIMIT:
#         break
