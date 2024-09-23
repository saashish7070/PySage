# read the data from the file
import json
from tokenizers import Tokenizer, normalizers
normalizer = normalizers.Sequence([
    normalizers.NFD(),
    normalizers.StripAccents()
])
import unicodedata
def read_data(file_paths, get_content):
    '''
    return - JSON object
    '''
    for file in file_paths:
        with open(file, 'r') as f:
            for line in f:
                json_data = json.loads(line)
                content = get_content(json_data)
                yield content


file_paths = ['./math/train.jsonl']
i = 0
count = {}

for content in read_data(file_paths, lambda s: s['text']):
    # i += 1
    # if i > 5000:
    #     break
    content = unicodedata.normalize('NFKC', content)
    for character in list(content):
        if character not in count:
            count[character] = 1
        else:
            count[character] +=1

with open('info.json', 'w') as f:
    f.write(json.dumps(count))
print(len(count.keys()))