def is_clean(text):


    # Check if character is in CJK Unified Ideographs, Hiragana, Katakana, Hangul ranges
    for char in text:
        if '\u4e00' <= char <= '\u9fff' or \
        '\u3040' <= char <= '\u309f' or  \
        '\u30a0' <= char <= '\u30ff' or  \
        '\uac00' <= char <= '\ud7af':     # Hangul Syllables (Korean)
            return False
    return True