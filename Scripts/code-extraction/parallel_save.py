import os
import json
from concurrent.futures import ThreadPoolExecutor
from datasets import load_dataset
from download import download_contents

# Function to process a single row
def process_row(i, row, supported_languages, output_file):
    # Convert repo_name to file (this is just a print for debugging)
    print(i, row['repo_name'])

    # Modify date fields to be ISO formatted strings
    row["visit_date"] = row["visit_date"].isoformat()
    row["revision_date"] = row["revision_date"].isoformat()
    row["committer_date"] = row["committer_date"].isoformat()

    row["gha_created_at"] = row["gha_created_at"].isoformat() if row["gha_created_at"] else ""
    row["gha_updated_at"] = row["gha_updated_at"].isoformat() if row["gha_updated_at"] else ""
    row["gha_pushed_at"] = row["gha_pushed_at"].isoformat() if row["gha_pushed_at"] else ""

    # Download file contents
    content = download_contents(row['files'], supported_languages)
    row['files'] = content['files']

    # Serialize the row to JSON and write to the output file
    string_data = json.dumps(row)
    output_file.write(string_data + "\n")

# Parallel processing function
def process_dataset(ds, supported_languages, output_dir, max_threads=5, max_limit=None):
    # Initialize the supported language count dictionary
    language_count = {language: 0 for language in supported_languages}

    # Open the output file for writing
    output_file_path = os.path.join(output_dir, "code.jsonl")
    with open(output_file_path, 'a') as output_file:
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = []
            for i, row in enumerate(ds):
                # Skip rows if language limit is reached
                # if i > max_limit:
                #     break
                
                # Increase the count of processed languages
                # language_count[row['gha_language']] += 1

                # Submit the processing task to the thread pool
                futures.append(executor.submit(process_row, i, row, supported_languages, output_file))

            # Wait for all threads to complete
            for future in futures:
                future.result()

# Main script
if __name__ == "__main__":
    # Load the dataset
    ds = load_dataset("bigcode/the-stack-v2-train-smol-ids", streaming=True, split="train")

    # Supported files
    supported_languages = ['Python']

    # Filter to only keep supported languages
    ds = ds.filter(lambda row: row['gha_language'] in supported_languages)

    # Set the output directory
    output_dir = "./new-python-dataset"

    # Set the maximum limit for each language
    MAX_LIMIT = 100000

    # Process the dataset in parallel
    process_dataset(ds, supported_languages, output_dir, max_threads=16, max_limit=MAX_LIMIT)