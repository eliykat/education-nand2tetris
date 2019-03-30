import sys

class JackTokenizer:

    symbols = [
        '{',
        '}',
        '(',
        ')',
        '[',
        ']',
        '.',
        ',',
        ';',
        '+',
        '-',
        '*',
        '/',
        '&',
        '|',
        '<',
        '>',
        '=',
        # Omitted - maybe an em dash - last character unknown, see p 246 of pdf
    ]

    keywords = [
        'class',
        'constructor',
        'function',
        'method',
        'field',
        'static',
        'var',
        'int',
        'char',
        'boolean',
        'void',
        'true',
        'false',
        'null',
        'this',
        'let',
        'do',
        'if',
        'else',
        'while',
        'return'
    ]

    def __init__(self, input):
        # Constructor - opens input file/stream and gets ready to tokenize it
        self.input = open(input)
        self.nextLine()

    def hasMoreTokens(self):
        # Returns true if there are more tokens in input

        # here's how you do this
        # save the cursor position in the file - this will be the start of the current line.
        # save self.line - this will be the current line (partially consumed)
        # then run getChar until we EITHER hit EOF (return false) or a valid char (return true)
        # then restore the cursor and self.line

        pass

    def getChar(self):
        """ Disposes of garbage in self.line and returns first valid char for analysis.
        Will not move past a valid char. """

        # If line is empty or commented, move to the next line and try again
        if len(self.line) == 0 or self.line[0:2] == "//":
            self.nextLine()
            self.getChar()

        # If start of block comment, search for the end of the comment and try again
        if self.line[0:2] == "/*":
            while self.line.find("*/") == -1:
                self.nextLine()

            # move one line past the end of the comment
            self.nextLine()

        # If char is space, remove it and try again
        if self.line[0] == " ":
            self.line = self.line[1:]
            self.getChar()

        # Return valid char for analysis
        return self.line[0]

    def advance(self):
        # Gets the next token from input and stores in self.token

        testChar = self.getChar()

        if testChar.isalpha():

            # Find index of last character of token
            for count, char in enumerate(self.line):
                if not char.isalpha() and not char.isnumeric() and char != '_':
                    tokenEnd = count
                    break

        elif testChar.isnumeric():
            # Find index of last character of token
            for count, char in enumerate(self.line):
                if not char.isnumeric():
                    tokenEnd = count
                    break

        elif testChar in JackTokenizer.symbols:
            tokenEnd = 1

        else:
            print('Error - invalid token')
            print(self.line)
            sys.exit()

        self.token = self.line[:tokenEnd]
        self.line = self.line[tokenEnd:]

    def tokenType(self):
        # Returns the type of the current token
        if self.token.upper() in JackTokenizer.keywords:
            return 'KEYWORD'
        elif self.token in JackTokenizer.symbols:
            return 'SYMBOL',
        elif self.token[0] == '"' and self.token[len(self.token)] == '"':
            return 'STRING_CONST'
        elif self.token.isnumeric():
            return 'INT_CONST'
        else:
            return 'IDENTIFIER'

    def keyWord(self):
        # Returns the keyword which is the current token (only if tokenType() == keyword)
        return self.token.upper()

    def symbol(self):
        # Returns the character which is the current token (only if tokenType() == symbol)
        return self.token

    def identifier(self):
        # Returns the identifier which is the current token (only if tokenType() == identifier)
        return self.token

    def intVal(self):
        # Returns the integer value of the current token (only if tokenType() == int_const)
        return self.token

    def stringVal(self):
        # Returns the string value of the current token, without double quotes (only if tokenType() = string_const)
        return self.token[1:len(self.token) - 1]

    def nextLine(self):
        """Read next line in file"""
        self.line = self.input.readline().strip()
