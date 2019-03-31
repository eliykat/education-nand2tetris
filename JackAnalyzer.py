import sys
import os
from JackTokenizer import JackTokenizer

def main():
    try:
        input = sys.argv[1]
    except IndexError:
        print("Error: you must supply a file for analyzing")
        sys.exit()

    tokenizer = JackTokenizer(input)

    while tokenizer.hasMoreTokens():
        tokenizer.advance()
        print(tokenizer.token)

    tokenizer.close()
    

if __name__ == '__main__':
    main()