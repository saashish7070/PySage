# original test cases
a = '''Hello how are you""'''
b = """Hello how are you'' ?"""
c = 'Hello "world"'
d = "Python's awesome"
e = '''Multi-line "string"'''
f = """Another 'multi-line' string"""
g = """Hello how are you'' ?"""
h = "Hello \"world\""
i = "Python\'s awesome"
j = """Multi-line "string\""""
k = """Another 'multi-line' string"""
# normalized test cases
a = """Hello how are you"\""""
b = """Hello how are you'' ?"""
c = "Hello \"world\""
d = "Python's awesome"
e = """Multi-line "string\""""
f = """Another 'multi-line' string"""
g = """Hello how are you'' ?"""
h = "Hello \"world\""
i = "Python\'s awesome"
j = """Multi-line "string\""""
k = """Another 'multi-line' string"""