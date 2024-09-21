import gzip
import jsonlines

def read_gzip_jsonl(file_path, is_clean):
    json_lines = []
    with gzip.open(file_path, 'rt', encoding='utf-8') as compressed_file:
        with jsonlines.Reader(compressed_file) as json_reader:
            for obj in json_reader:
                if is_clean(obj):
                    json_lines.append(obj)
    return json_lines