import sys
import os
from CompilationEngine import CompilationEngine

def main():
    try:
        input = sys.argv[1]
    except IndexError:
        print("Error: you must supply a file for analyzing")
        sys.exit()

    output = input[:input.rfind('.')] + '-mine.xml'

    CompilationEngine(input, output)

if __name__ == '__main__':
    main()