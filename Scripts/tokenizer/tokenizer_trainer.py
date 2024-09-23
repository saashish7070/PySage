from tokenizers.trainers import BpeTrainer
from tokenizer import tokenizer

tokenizer_save_path = './tokenizer.json'
data_path = './test.jsonl'

def read_jsonl(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            yield line

# Define special tokens if necessary
special_tokens = ["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"]

tainer = BpeTrainer(vocab_size=20256, special_tokens=special_tokens)

tokenizer.train_from_iterator()

tokenizer.save(tokenizer_save_path)