import gzip
import jsonlines

def read_gzip_jsonl(file_path):
    with gzip.open(file_path, 'rt', encoding='utf-8') as compressed_file:
        with jsonlines.Reader(compressed_file) as json_reader:
            for obj in json_reader:
                print(obj)


file_path = 'datasets--hoskinson-center--proof-pile/snapshots/490b980249446f2f3bd2df3a8cf085d0f2de240a/dev/proofpile_dev.jsonl.gz'

read_gzip_jsonl(file_path)