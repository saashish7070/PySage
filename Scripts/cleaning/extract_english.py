# extract the english data set from the file
import os
import json

from read_zst import read_zst_jsonl
from clean_english import is_clean

# max training data in bytes
MAX_SIZE = 4 * 2**30 # 4 GB

# directory to save the output
base_out_dir = './english'

# max output size in bytes
max_sizes = {
    'train': MAX_SIZE, # 4 GB
    'test': MAX_SIZE // 8,  # 128 MB
    'validation': MAX_SIZE //8    # 128 MB
}

# Base path to your dataset directory
base_path = 'datasets--cerebras--SlimPajama-627B/snapshots/2d0accdd58c5d5511943ca1f5ff0e3eb5e293543'

# Define the splits
splits = ['test', 'validation']

# save the data to the file
def save_data(f, new_data):
    
    """
    save new_data to file
        return = True if successful else false
    """
        
    for entry in new_data:
        json_entry = json.dumps(entry)
        f.write(json_entry+'\n')
    
# Function to read and print chunks from a given split
def process_split(split_name, out_file):
    split_path = os.path.join(base_path, split_name)
    f = open(out_file, 'a')

    if not os.path.exists(split_path):
        print(f"Split {split_name} does not exist.")
        return
    
    chunks = os.listdir(split_path)

    # Iterate over chunks
    for chunk in chunks:
        chunk_path = os.path.join(split_path, chunk)

        files = os.listdir(chunk_path)
        for file in files:
            filePath = os.path.join(chunk_path, file)
            # if filePath exceeds max size return from the function
            size_of_file  = os.path.getsize(out_file)
            print(f"{out_file} size = {size_of_file/10**3}")
            if size_of_file > max_sizes[split_name]:
                f.close()
                return
            # Read and print content (assuming text files)
            data = read_zst_jsonl(filePath, is_clean) 
            if not data:
                continue
            save_data(f, data)

    f.close()          

            


# Read and print data for each split
for split in splits:
    if not os.path.exists(base_out_dir):
        print("Create the base dir ")
        break
    save_dir = os.path.join(base_out_dir, f"{split}.jsonl")
    process_split(split, save_dir)