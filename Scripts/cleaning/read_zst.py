import zstandard as zstd
import jsonlines

def read_zst_jsonl(file_path):
    # Open the Zstandard compressed file
    with open(file_path, 'rb') as compressed_file:
        # Create a Zstandard decompressor
        dctx = zstd.ZstdDecompressor()
        # Decompress the file
        with dctx.stream_reader(compressed_file) as reader:
            # Read and decode the decompressed data
            with jsonlines.Reader(reader) as json_reader:
                # Iterate over the JSON Lines entries
                for obj in json_reader:
                    print(obj)  # Process the JSON object as needed

# Path to the compressed JSON Lines file
file_path = 'datasets--cerebras--SlimPajama-627B/snapshots/2d0accdd58c5d5511943ca1f5ff0e3eb5e293543/test/chunk1/example_holdout_0.jsonl.zst'

# Read and print the contents
read_zst_jsonl(file_path)