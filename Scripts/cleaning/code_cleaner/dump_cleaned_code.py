import json
from typing import List, Dict, Any, Generator
import logging
import os

def load_data(
    file_path: str, 
    previous_idx: int = 0, 
    chunk_size: int = 30000
) -> Generator[List[Dict[str, Any]], None, None]:
    """
    Load data from JSONL file in chunks.
    
    Args:
        file_path (str): Path to JSONL file
        previous_idx (int): Index to start reading from
        chunk_size (int): Number of lines to read
    
    Returns:
        Generator yielding lists of repository data
    """
    try:
        with open(file_path, 'r') as f:
            # Skip to previous index
            for _ in range(previous_idx):
                next(f, None)
            
            code = []
            for line in f:
                json_code = json.loads(line)
                code.append(json_code)
                
                if len(code) == chunk_size:
                    yield code
                    code = []
            if code:
                yield code
        
    except IOError as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return []
    

# write the code to a file
with open('data.txt', 'w') as f:
    code_dir='new-python-dataset/syntax_free_repos'
    data_files=os.listdir(code_dir)
    files_to_read=3

    for i in range(files_to_read):
        data_file=data_files[i]
        data_file_path=os.path.join(code_dir, data_file)
        data=load_data(data_file_path)
        for chunk in data:
            for repo in chunk:
                for file in repo['files']:
                    f.write(file['content'])