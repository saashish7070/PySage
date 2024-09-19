import os
from read_gz import read_gzip_jsonl

# Base path to your dataset directory
base_path = 'datasets--hoskinson-center--proof-pile/snapshots/490b980249446f2f3bd2df3a8cf085d0f2de240a'

# Define the splits
splits = ['train', 'test', 'dev']

# Function to read and print chunks from a given split
def read_chunks(split_name):
    split_path = os.path.join(base_path, split_name)
    
    if not os.path.exists(split_path):
        print(f"Split {split_name} does not exist.")
        return
    
    files = os.listdir(split_path)

    # Iterate over chunks
    for file in files:
        if file == '.gitattributes':
            continue
        filePath = os.join(split_path, file)
    
        # Read and print content (assuming text files)
        read_gzip_jsonl(filePath)            

# Read and print data for each split
for split in splits:
    print(f"Reading {split} split:")
    read_chunks(split)