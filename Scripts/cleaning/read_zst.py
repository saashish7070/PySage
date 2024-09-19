import zstandard as zstd
import jsonlines
import io

def read_zst_jsonl(file_path, filter_rule=None):
    out = []
    # Open the Zstandard compressed file
    with open(file_path, 'rb') as compressed_file:
        # Create a Zstandard decompressor
        dctx = zstd.ZstdDecompressor()
        # Decompress the file
        with dctx.stream_reader(compressed_file) as reader:
            # wrap the binary stream with a text wrapper to decode it as UTF=-8
            text_stream=io.TextIOWrapper(reader, encoding='utf-8')
            # Read and decode the decompressed data
            with jsonlines.Reader(text_stream) as json_reader:
                # Iterate over the JSON Lines entries
                for obj in json_reader:
                    if not filter_rule(obj):
                        # print(obj["text"])
                        continue
                    out.append(obj)
    return out
# # Path to the compressed JSON Lines file
# file_path = 'datasets--cerebras--SlimPajama-627B/snapshots/2d0accdd58c5d5511943ca1f5ff0e3eb5e293543/test/chunk1/example_holdout_0.jsonl.zst'

# # Read and print the contents
# read_zst_jsonl(file_path)