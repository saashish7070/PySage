import os
from read_zst import read_zst_jsonl

# Base path to your dataset directory
base_path = 'datasets--cerebras--SlimPajama-627B/snapshots/2d0accdd58c5d5511943ca1f5ff0e3eb5e293543'

# Define the splits
splits = ['train', 'test', 'validation']

# Function to read and print chunks from a given split
def read_chunks(split_name):
    split_path = os.path.join(base_path, split_name)
    
    if not os.path.exists(split_path):
        print(f"Split {split_name} does not exist.")
        return
    
    chunks = os.listdir(split_path)

    # Iterate over chunks
    for chunk in chunks:
        files = os.listdir(split_path)

        for file in files:
            filePath = os.join(split_path, chunk, file)
        
            # Read and print content (assuming text files)
            read_zst_jsonl(filePath)            

# Read and print data for each split
for split in splits:
    print(f"Reading {split} split:")
    read_chunks(split)
