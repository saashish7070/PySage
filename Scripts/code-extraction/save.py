from datasets import load_dataset
from smart_open import open
import json
from datetime import datetime
# local imoport
from download import download_contents

output_dir = './python-dataset'
MAX_LIMIT = 10
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

# only keep python files
ds.filter(lambda row: row['gh_language'] == 'Python')

def serialize_data(row):
    serialized_row = {}
    for key, value in row.items():
        if isinstance(value, datetime):
            serialized_row[key] = value.isoformat()
        else:
            serialized_row[key] = value

    return serialized_row

for i, row in enumerate(ds):

    # remove the "files" key from the metadata as individiual file will have it
    content = download_contents(row['files'])

    repo_name = row['repo_name'].split('/')[-1]
    print(repo_name)
    # for key, value in row.items():
    #     print(f"{key}: {type(value)}")
    with open(f"{output_dir}/{repo_name}.json", 'w') as f:
        
        row['files'] = content['files']
        string_data = json.dumps(serialize_data(row))
        f.write(string_data)
    
    if i == MAX_LIMIT:
        break