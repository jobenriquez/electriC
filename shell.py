import lexer
from sys import *

try:
    lexer.read(argv[1])
except FileNotFoundError:
    print(f"File not found error: File '{argv[1]}' cannot be located.")


