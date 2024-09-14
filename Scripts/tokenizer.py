import datasets
from datasets import load_dataset

import transformers
from transformers import AutoTokenizer
import torch

# load the dataset
ds = load_dataset('cerebras/SlimPajama-627B', 
                  streaming=True, 
                  split='validation')

# load pretrained tokenizer
tokenizer = AutoTokenizer.from_pretrained('deepseek-ai/DeepSeek-Coder-V2-Lite-Base',
                                           trust_remote_code=True)


# ds.save_to_disk('./slimPajama-validation')