import unicodedata

char = '３'  # The Unicode character
print(f"Character: {char}")
print(f"Name: {unicodedata.name(char)}")
print(f"Code Point: U+{ord(char):04X}")
