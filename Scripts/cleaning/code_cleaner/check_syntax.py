import ast
import json
import time
import logging
import multiprocessing as mp
from typing import List, Dict, Any, Generator
import os

# format  of repository jsonl file
'''
{
    "repo_name": <str>,
    "repo_url": <str>,
    "gha_language": <str>,
    "files": [
        {
            "blob_id": <str>,
            "path": <str>,
            "content_id": <str>,
            "language": <str>,
            "length_bytes": <int>,
            "detected_licenses": <list>,
            "license_type": <str>,
            "src_encoding": <str>,
            "is_vendor": <bool>,
            "is_generated": <bool>,
            "alphanum_fraction": <float>,
            "alpha_fraction": <float>,
            "num_lines": <int>,
            "avg_line_length": <float>,
            "max_line_length": <int>,
            "content": <str>
        }
    ]
}
'''

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('syntax_check.log'),
        logging.StreamHandler()
    ]
)

# workflow for each process

# 1 for each chunk check syntax
# 2 write to file according to process id


def attempt_syntax_fix(code: str) -> tuple[bool, str]:
    """
    Attempt to fix common syntax errors in Python code.
    
    Args:
        code (str): Python code to fix
    
    Returns:
        tuple[bool, str]: (True if fixed successfully, fixed code)
    """
    try:
        # First try original code
        ast.parse(code)
        return True, code
    except SyntaxError as e:
        # Common fixes to attempt
        fixes = [
            lambda c: c.replace('´', "'"),  # Fix wrong quote characters
            lambda c: c.replace('"', '"').replace('"', '"'),  # Fix smart quotes
            lambda c: c.replace('…', '...'),  # Fix ellipsis
            lambda c: c.rstrip() + '\n',  # Add missing newline at EOF
            lambda c: c + 'pass\n' if c.rstrip().endswith(':') else c,  # Add pass to empty blocks
            lambda c: c.replace('−', '-'),  # Fix minus sign
            lambda c: c.replace('\t', '    '),  # Replace tabs with spaces
        ]
        
        # Try each fix
        for fix in fixes:
            try:
                fixed_code = fix(code)
                ast.parse(fixed_code)
                return True, fixed_code
            except SyntaxError:
                continue
            
    return False, code

def check_syntax(code: str) -> tuple[bool, str]:
    """
    Check Python syntax and attempt to fix if there's an error.
    
    Args:
        code (str): Python code to check
    
    Returns:
        tuple[bool, str]: (True if valid syntax, potentially fixed code)
    """
    try:
        ast.parse(code)
        return True, code
    except SyntaxError:
        return attempt_syntax_fix(code)
    except (ValueError, TypeError):
        return False, code

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

def process_chunk(data: List[Dict[str, Any]]) -> List[str]:
    """
    Process a chunk of repository data and return syntax-free repos.
    """
    out = []
    for repo in data:
        is_syntax_free = True
        python_files = []
        for file in repo['files']:
            if 'content' not in file:
                is_syntax_free = False
                break
                
            is_valid, fixed_code = check_syntax(file['content'])
            if is_valid:
                file['content'] = fixed_code  # Use fixed version if successful
                python_files.append(file)
            else:
                is_syntax_free = False
                break
                
        if is_syntax_free and python_files:
            repo['files'] = python_files
            out.append(repo)

    return out


def write_repos(repos: List[str], output_path: str):
    """
    Write syntax-free repository names to a file.
    
    Args:
        repos (List[str]): Repository names
        output_path (str): Path to output file
    """
    with open(output_path, 'a') as f:
        for repo in repos:
            f.write(json.dumps(repo) + '\n')

# task for each process
def process_task(
    data: List[Dict[str, Any]], 
    output_dir: str,
    process_idx: int
) -> float:
    """
    Process data chunks using multiprocessing.
    
    Args:
        data (List[Dict]): Repository data
        output_dir (str): Directory to write output files
        process_idx (int): Index of process
    
    Returns:
        float: Total processing time
    """
    result = process_chunk(data) # repos with valid syntax

    # for each process, write to a different file
    write_repos(result, f'{output_dir}/syntax_free_repos_{process_idx}.jsonl')
    

def main():
    input_file = './new-python-dataset/code.jsonl'
    output_dir = './new-python-dataset/syntax_free_repos2'
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Load data
    generator = load_data(input_file, 0, 18000)
    
    logging.info("Starting Multiprocessing Syntax Check")
    start_time = time.time()
    
    # Determine optimal number of processes
    num_workers = min(mp.cpu_count(), 9)
    logging.info(f"Using {num_workers} processes")
    for i, repos in enumerate(generator):

        chunks = [repos[i::num_workers] for i in range(num_workers)]
        with mp.Pool(processes=num_workers) as pool:
            pool.starmap(process_task, [(chunk, output_dir, i) for i, chunk in enumerate(chunks)])
        # log the time taken for each chunk
        logging.info(f"Time taken for {i+1}th chunk of {len(repos)} repositories: {time.time() - start_time:.4f} seconds")
        # Periodically log the progress
        logging.info(f"Processed {(i+1)*len(repos)} repositories")

    logging.info(f"Processing completed in {time.time() - start_time:.4f} seconds")



if __name__ == "__main__":
    main()

