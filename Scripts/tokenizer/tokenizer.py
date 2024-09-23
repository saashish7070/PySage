import re
from tokenizers import Tokenizer, normalizers
from tokenizers.models import BPE
from tokenizers.pre_tokenizers import ByteLevel, Sequence, Digits


# Initialize tokenizer and trainer
tokenizer = Tokenizer(BPE())


# Define a custom normalizer to replace more than three consecutive line breaks with one
class ReplaceMultipleLineBreaks(normalizers.Normalizer):
    def normalize(self, normalized):
        # Use regex to match more than 3 consecutive line breaks and replace with 1
        normalized = re.sub(r'(\n\s*){3,}', '\n', normalized)
        return normalized
    
    def normalize_str(self, sequence):
        return self.normalize(sequence)
    
hello = ReplaceMultipleLineBreaks()

# Define your sequence of normalizers for code generation
tokenizer.normalizer = normalizers.Sequence([
    normalizers.NFC(),  # Normalize Unicode to composed form
    normalizers.Strip(left=True, right=True),  # Trim whitespace at the start and end
    normalizers.Replace(pattern="\r\n", content="\n"),  # Normalize newlines
    ReplaceMultipleLineBreaks(),    # multiple_linebreak_normalizer
])


tokenizer.pre_tokenizer = Sequence([ByteLevel(), Digits(individual_digits=True)])  # avoids digit from merging

