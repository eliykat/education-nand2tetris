import sys
from TokenTypeError import TokenTypeError

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
        '~'
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
        self.lineNo = 0

        print("Opened " + input + " for tokenizing")

        self.nextLine()

    def hasMoreTokens(self):
        # Returns true if there are more tokens in input

        if self.getChar() is not None:
            return True
        else:
            return False

    def getChar(self):
        """ Disposes of garbage in self.line and returns first valid char for analysis (being a char that belongs to a token).
        Will not move past a valid char. """

        # print(repr(self.line))
        
        # Test for EOF (indicated by empty string without newline char)
        if not self.line and "\n" not in self.line:
            return None

        # If line is empty or commented, move to the next line and try again
        elif self.line == "\n" or self.line[0:2] == "//":
            self.nextLine()
            return self.getChar()

        # If start of block comment, search for the end of the comment and try again
        elif self.line[0:2] == "/*":
            while "*/" not in self.line:
                self.nextLine()

            # move one line past the end of the comment
            self.nextLine()

            return self.getChar()

        # If char is space, remove it and try again
        elif self.line[0] == " ":
            self.line = self.line[1:]
            return self.getChar()

        # Base case - this is a valid char to pass up the chain
        else:
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

        elif testChar == '"':
            tokenEnd = self.line.index('"', 1) + 1
        
        else:
            print('Error - invalid token')
            print(self.lineNo)
            print('"' + self.line + '"')
            sys.exit()

        self.token = self.line[:tokenEnd]
        self.line = self.line[tokenEnd:]

    def lookAhead(self):
        # Returns the next token without advancing
        # Created to solve challenges with CompilationEngine.compileTerm()

        currentLine = self.line
        currentToken = self.token

        self.advance()
        nextToken = self.token

        self.line = currentLine
        self.token = currentToken

        return nextToken

    def tokenType(self):
        # Returns the type of the current token
        if self.token.lower() in JackTokenizer.keywords:
            return 'KEYWORD'
        elif self.token in JackTokenizer.symbols:
            return 'SYMBOL'
        elif self.token[0] == '"':
            return 'STRING_CONST'
        elif self.token.isnumeric():
            return 'INT_CONST'
        else:
            return 'IDENTIFIER'

    def keyWord(self):
        # Returns the keyword which is the current token (only if tokenType() == keyword)
        if self.tokenType() == 'KEYWORD':
            return self.token.upper()
        else:
            raise TokenTypeError('KEYWORD', self.tokenType(), self.token, self.lineNo)

        # Type checking disabled because it includes user-defined classes, which I am not dealing with at this stage

        # return self.token.upper()

    def symbol(self):
        # Returns the character which is the current token (only if tokenType() == symbol)
        if self.tokenType() == 'SYMBOL':
            return self.token
        else:
            raise TokenTypeError('SYMBOL', self.tokenType(), self.token, self.lineNo)

    def identifier(self):
        # Returns the identifier which is the current token (only if tokenType() == identifier)
        if self.tokenType() == 'IDENTIFIER':
            return self.token
        else:
            raise TokenTypeError('IDENTIFIER', self.tokenType(), self.token, self.lineNo)

    def intVal(self):
        # Returns the integer value of the current token (only if tokenType() == int_const)
        if self.tokenType() == 'INT_CONST':
            return self.token
        else:
            raise TokenTypeError('INT_CONST', self.tokenType(), self.token, self.lineNo)

    def stringVal(self):
        # Returns the string value of the current token, without double quotes (only if tokenType() = string_const)
        if self.tokenType() == 'STRING_CONST':
            return self.token[1:len(self.token) - 1]
        else:
            raise TokenTypeError('STRING_CONST', self.tokenType(), self.token, self.lineNo)

    def nextLine(self):
        """Read next line in file, stripped of spaces and tabs"""

        # Note that this may not work if there are spaces and tabs interspersed
        self.line = self.input.readline().strip(' ').strip('\t')
        self.lineNo += 1

    def close(self):
        self.input.close()
        print("Tokenizing finished.")