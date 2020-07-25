import sys
import os
from CompilationEngine import CompilationEngine

class InputFileError(Exception):
    """Exception if an illegal token is encountered"""
    def __init__(self, message):
        self.message = message

def main():
    try:
        input = sys.argv[1]
    except IndexError:
        print("Error: you must supply a file for compiling")
        sys.exit()

    if os.path.isdir(input):
        # Directory of files to compile

        if input.endswith('\\') == False:
            input = input + '\\'

        for inputFile in os.listdir(input):
            if inputFile.endswith('.jack'):

                outputFile = inputFile[:inputFile.rfind('.')] + '.vm'

                CompilationEngine(input + inputFile, input + outputFile)
                
    elif os.path.isfile(input):
        # Single file to compile
        if input.endswith('.jack') == False:
            raise InputFileError('Input file is not recognised as a .jack file type')

        output = input[:input.rfind('.')] + '.vm'

        CompilationEngine(input, output)

    else:
        # Exit
        raise InputFileError('Input is not a directory or file')

if __name__ == '__main__':
    main()