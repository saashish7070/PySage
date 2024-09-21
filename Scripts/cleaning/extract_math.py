import os
import json

from read_gz import read_gzip_jsonl
from clean_math import is_clean
# Base path to your dataset directory
base_path = 'datasets--hoskinson-center--proof-pile/snapshots/490b980249446f2f3bd2df3a8cf085d0f2de240a'

# Define the splits
splits = ['train', 'test', 'dev']

# max training data in bytes
MAX_SIZE = 2 * 2**26 # 2 GB

# directory to save the output
base_out_dir = './math'

# max output size in bytes
max_sizes = {
    'train': MAX_SIZE, 
    'test': MAX_SIZE // 8, 
    'dev': MAX_SIZE //8    
}

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
    
    files = os.listdir(split_path)

    # Iterate over chunks
    for file in files:
        if file == '.gitattributes':
            continue

        filePath = os.path.join(split_path, file)

        # if filePath exceeds max size return from the function
        size_of_file  = os.path.getsize(out_file)
        print(f"{out_file} size = {size_of_file/10**3}")
        if size_of_file > max_sizes[split_name]:
            f.close()
            return
        # Read and print content (assuming text files)
        data = read_gzip_jsonl(filePath, is_clean) 

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