import json
from packed_dataset import PackedDataset
from packed_dataset import PackedDatasetBuilder
from transformers import Tokenizer
import numpy as np

tokenizer_path = ''

tokenizer = Tokenizer.from_file(tokenizer_path)
# Dataset Loader
class EnglishDataset(PackedDataset):

    def __init__(self, filenames, n_chunks, block_size, tokenizer, **kwargs):
        self.tokenzier
        super().__init__(filenames, n_chunks, block_size, **kwargs)
    
    
    def __iter__(self):
        for file in self.__filenames:
            with open(file, 'r') as f:
                for line in f:
                    data = json.loads(line)
                    text = data["text"]
                    token_ids=self.tokenizer.encode(text)

                    yield token_ids



def process_data(dataset, destination_path, chunk_size):
    builder=PackedDatasetBuilder(
        outdir=destination_path,
        prefix="processed_data",
        chunk_size=chunk_size,
        sep_token=tokenizer.bos_token_id,
        dtype="auto",
        vocab_size=tokenizer.vocab_size
    )

    for token_ids in dataset:
        builder.add_array(np.array(token_ids, dtype=builder.dtype))

