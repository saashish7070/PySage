# define the cleaning function for english corpus
import random

def is_english(text, threshold=0.9, allow_numbers=True, allow_symbols=True, rejection_inspection_prob=0.01):

    allowed_chars  =set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')

    # allow new lines and tabs
    allowed_chars.update('\n\t')
    if allow_numbers:
        allowed_chars.update('0123456789')

    if allow_symbols:
        allowed_chars.update(' ~&-@<—>%=£*^+#_|$.,;:!?"\'(©)-{}[–]`/\\…')
    

    is_valid=all( char in allowed_chars for char in text )
    
    
    #  Calculate the ratio of valid characters (alphanumeric + whitespace)
    valid_ratio = sum(c.isalnum() or c.isspace() for c in text) / len(text) if text else 0
    
    decision = is_valid and valid_ratio > threshold 
    if not is_valid and random.random() < rejection_inspection_prob:
        # print(f"Rejected text (for inspection): {text}")
        print("Rejected characters:", set(char for char in text if char not in allowed_chars))
    
    # return true if valid_ratio < threshold and characters are within the allowed_char set
    return decision

def is_clean(text):
    source = text["meta"]["redpajama_set_name"]
    return source != 'RedPajamaGithub' \
            and source != "RedPajamaArXiv" \
            and is_english(text["text"])