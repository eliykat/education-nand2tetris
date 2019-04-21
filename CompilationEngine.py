from JackTokenizer import JackTokenizer
from lxml import etree
from TokenTypeError import TokenTypeError
from SymbolTable import SymbolTable

class CompilationEngine():

    op = ['+', '-', '*', '/', '&', '|', '<', '>', '=']

    def __init__(self, input, output):
        self.input = input
        self.output = open(output, 'w')
        self.tokenizer = JackTokenizer(input)
        self.symbolTable = SymbolTable()

        self.tokenizer.advance()

        # Compile the class (should not be any other token)
        self.compileClass()

    def subTag(self, _tag):
        result = etree.SubElement(self.pointer, _tag)

        if _tag == 'keyword':
            result.text = self.tokenizer.keyWord().lower()
        elif _tag == 'symbol':
            result.text = self.tokenizer.symbol()
        # elif _tag == 'identifier':
        #     result.text = self.tokenizer.identifier()
        elif _tag == 'integerConstant':
            result.text = self.tokenizer.intVal()
        elif _tag == 'stringConstant':
            result.text = self.tokenizer.stringVal()
        # else:
        #     result.text = '' # Force empty tags - for compatibility with comparison file

        return result

    def subTagIdentifier(self, name, category, new, kind, index):
        self.pointer = self.subTag('identifier')

        # Name
        etree.SubElement(self.pointer, 'name').text = name

        # Category: var, argument, static, field, class, subroutine
        etree.SubElement(self.pointer, 'category').text = category

        # Is it newly defined? Boolean
        etree.SubElement(self.pointer, 'new').text = new

        # Kind: var, argument, static, field (if applicable)
        etree.SubElement(self.pointer, 'kind').text = kind

        # Index: unique index
        etree.SubElement(self.pointer, 'index').text = str(index)

        self.pointer = self.pointer.getparent()
    
    def compileClass(self):
        # Current token assumed to be the CLASS keyword
    
        # Class XML tag and move pointer
        self.pointer = etree.Element('class')

        # Keyword: class
        self.subTag('keyword')
        self.tokenizer.advance()

        # Identifier: class name
        # Classes are not entered into symboltable
        self.subTagIdentifier(
            self.tokenizer.identifier(),
            'CLASS',
            'TRUE',
            'NONE',
            'NONE'
        )
        self.tokenizer.advance()

        # Symbol: {
        self.subTag('symbol')
        self.tokenizer.advance()

        # classVarDec or Subroutine
        while not self.tokenizer.token == '}':      # Access token directly to circumvent error checking
            if self.tokenizer.keyWord() in ['STATIC', 'FIELD']:
                self.compileClassVarDec()
            elif self.tokenizer.keyWord() in ['CONSTRUCTOR', 'FUNCTION', 'METHOD']:
                self.compileSubroutine()

        # Symbol: }
        self.subTag('symbol')

        self.close()

        # Move pointer up to parent
        # self.pointer = self.pointer.getparent()

        # # Move to the next token (which should only be a class declaration) if available, otherwise finish compilation
        # if self.tokenizer.hasMoreTokens():
        #     self.tokenizer.advance()
        #     self.compileClass()
        # else:
        #     self.close()

    def close(self):
        self.tokenizer.close()

        ## Write to output file and close
        # This is convoluted but the lxml pretty printing does not work properly
        string = etree.tostring(self.pointer, pretty_print=True, encoding='unicode')
        string = string.replace('<expressionList/>', '<expressionList>\n</expressionList>')
        string = string.replace('<parameterList/>', '<parameterList>\n</parameterList>')

        self.output.write(string)
        self.output.close()
        self.tokenizer.close()

        print('CompilationEngine complete.')
    
    def compileClassVarDec(self):
        # Current token assumed to be the STATIC or FIELD keyword

        # Create XML tag and move pointer
        self.pointer = self.subTag('classVarDec')

        # Keyword: STATIC or FIELD
        self.subTag('keyword')
        self.tokenizer.advance()

        # Keyword: type | identifier (if class)
        try:
            _type = self.tokenizer.keyWord()
            self.subTag('keyword')
        except TokenTypeError:
            _type = self.tokenizer.identifier()
            self.subTagIdentifier(
                self.tokenizer.identifier(),
                'CLASS',
                'FALSE',
                self.symbolTable.kindOf(self.tokenizer.identifier()),
                self.symbolTable.indexOf(self.tokenizer.identifier())
            )
        self.tokenizer.advance()

        # Identifier: varName
        # Declare in symboltable
        self.symbolTable.define(
            self.tokenizer.identifier(),
            _type,
            'FIELD'
        )
        self.subTagIdentifier(
            self.tokenizer.identifier(),
            'FIELD',
            'TRUE',
            _type,
            self.symbolTable.indexOf(self.tokenizer.identifier())
        )
        self.tokenizer.advance()

        # Compile any other varDecs on the same line (of the same type)
        while self.tokenizer.symbol() == ',':
            self.subTag('symbol')
            self.tokenizer.advance()
            
            # Identifier: varName
            # Declare in symboltable
            self.symbolTable.define(
                self.tokenizer.identifier(),
                _type,
                'FIELD'
            )
            self.subTagIdentifier(
                self.tokenizer.identifier(),
                'FIELD',
                'TRUE',
                _type,
                self.symbolTable.indexOf(self.tokenizer.identifier())
            )
            self.tokenizer.advance()

        # Symbol: ;
        self.subTag('symbol')

        self.tokenizer.advance()

        # Move pointer back up
        self.pointer = self.pointer.getparent()       

    def compileSubroutine(self):
        # Current token assumed to be keyword: constructor | function | method | void | <type>

        # Create new subroutine scoped symbol table
        self.symbolTable.startSubroutine()
    
        # Create XML element and move pointer
        self.pointer = self.subTag('subroutineDec')

        # Keyword: constructor | function | method 
        self.subTag('keyword')
        self.tokenizer.advance()

        # Keyword: void | identifier (if class)
        try:
            self.tokenizer.keyWord()
            self.subTag('keyword')
        except TokenTypeError:
            self.subTagIdentifier(
                self.tokenizer.identifier(),
                'CLASS',
                'FALSE',
                'NONE',
                'NONE'
            )

        # Identifier: subroutineName
        self.tokenizer.advance()
        self.subTagIdentifier(
            self.tokenizer.identifier(),
            'SUBROUTINE',
            'TRUE',
            'NONE',
            'NONE'
        )

        # Symbol: (
        self.tokenizer.advance()
        self.subTag('symbol')

        # Program structure: ParameterList
        self.tokenizer.advance()
        self.compileParameterList()

        # Symbol: )
        self.subTag('symbol')
        self.tokenizer.advance()

        ### START SUBROUTINE BODY ###
        self.pointer = self.subTag('subroutineBody')

        # Symbol: {
        self.subTag('symbol')
        self.tokenizer.advance()

        # subroutineBody: varDecs
        while self.tokenizer.keyWord() == 'VAR':
            self.compileVarDec()
        
        # subroutineBody: Statements
        self.compileStatements()

        # Symbol: }
        self.subTag('symbol')

        # Move pointer up
        self.pointer = self.pointer.getparent()

        ### END SUBROUTINE BODY ###

        self.tokenizer.advance()

        # Move pointer up
        self.pointer = self.pointer.getparent()

    def compileParameterList(self):
        # assume pointer is on keyword: type of first parameter OR symbol: ( if no parameters

        # Create XML tree and descend into it
        self.pointer = self.subTag('parameterList')

        if self.tokenizer.token is not ')':
            run_once = True
            while self.tokenizer.token == ',' or run_once == True:

                if run_once == False:
                    # Symbol: ,
                    self.subTag('symbol')
                    self.tokenizer.advance()
                
                # Keyword: type
                _type = self.tokenizer.keyWord()
                self.subTag('keyword')
                self.tokenizer.advance()

                # Identifier: varName
                # Declare in symboltable
                self.symbolTable.define(
                    self.tokenizer.identifier(),
                    _type,
                    'ARG'
                )
                self.subTagIdentifier(
                    self.tokenizer.identifier(),
                    'ARGUMENT',
                    'TRUE',
                    _type,
                    self.symbolTable.indexOf(self.tokenizer.keyWord())
                )
                self.tokenizer.advance()

                run_once = False

        # Ascend XML tree
        self.pointer = self.pointer.getparent()

    def compileVarDec(self):
        # assume pointer is on keyword: var

        # Create XML tree and descend
        self.pointer = self.subTag('varDec')

        # Keyword: var
        self.subTag('keyword')
        self.tokenizer.advance()

        # Keyword: type | identifier (if class)
        try:
            _category = self.tokenizer.keyWord()
            self.subTag('keyword')
        except TokenTypeError:
            _category = 'CLASS'
            self.subTagIdentifier(
                self.tokenizer.identifier(),
                'CLASS',
                'FALSE',
                'NONE',
                'NONE'
            )
        finally:
            self.tokenizer.advance()

        # Identifier: varName
        ## USING SYMBOLTABLE
        # Define in symboltable
        self.symbolTable.define(
            self.tokenizer.identifier(),
            _category,
            'VAR')
        self.subTagIdentifier(
            self.tokenizer.identifier(),
            'VAR',
            'TRUE',
            'VAR',
            self.symbolTable.indexOf( self.tokenizer.identifier() )
        )
        self.tokenizer.advance()

        # Further varNames
        while self.tokenizer.symbol() == ',':
            self.subTag('symbol')
            self.tokenizer.advance()
            
            self.symbolTable.define(
                self.tokenizer.identifier(),
                _category,
                'VAR')
            self.subTagIdentifier(
                self.tokenizer.identifier(),
                'VAR',
                'TRUE',
                'VAR',
                self.symbolTable.indexOf( self.tokenizer.identifier() )
            )
            self.tokenizer.advance()

        # Symbol: ;
        self.subTag('symbol')

        self.tokenizer.advance()

        # Ascend
        self.pointer = self.pointer.getparent()

    def compileStatements(self):
        # assume token is keyword: let | if | while | do | return

        # create XML tree and descend
        self.pointer = self.subTag('statements')

        # note: each of the nested compile methods call tokenizer.advance() at the end,
        # so no need to call it here

        while self.tokenizer.token is not '}':
            if self.tokenizer.keyWord() == 'LET':
                self.compileLet()
            elif self.tokenizer.keyWord() == 'IF':
                self.compileIf()
            elif self.tokenizer.keyWord() == 'WHILE':
                self.compileWhile()
            elif self.tokenizer.keyWord() == 'DO':
                self.compileDo()
            elif self.tokenizer.keyWord() == 'RETURN':
                self.compileReturn()
            else:
                raise TokenTypeError('Statement keyword', self.tokenizer.tokenType(), self.tokenizer.token, self.tokenizer.lineNo)

        self.pointer = self.pointer.getparent()

    def compileSubroutineCall(self):
        
        # As per page 211, this is not supposed to be its own sub-tree

        # Identifier: subroutineName or (className | varName)
        if self.tokenizer.lookAhead() == '.':
            self.subTagIdentifier(
                self.tokenizer.identifier(),
                'CLASS',
                'FALSE',
                self.symbolTable.kindOf(self.tokenizer.identifier()),
                self.symbolTable.indexOf(self.tokenizer.identifier())
            )
        else:
            self.subTagIdentifier(
                self.tokenizer.identifier(),
                'SUBROUTINE',
                'FALSE',
                self.symbolTable.kindOf(self.tokenizer.identifier()),
                self.symbolTable.indexOf(self.tokenizer.identifier())
            )

        # Symbol: . or (
        self.tokenizer.advance()
        self.subTag('symbol')

        # Additional tokens if subroutine is in another class or var
        if self.tokenizer.symbol() == ".":
            # Identifier: subroutineName
            self.tokenizer.advance()
            self.subTagIdentifier(
                    self.tokenizer.identifier(),
                    'SUBROUTINE',
                    'FALSE',
                    self.symbolTable.kindOf(self.tokenizer.identifier()),
                    self.symbolTable.indexOf(self.tokenizer.identifier())
                )

            # Symbol: (
            self.tokenizer.advance()
            self.subTag('symbol')

        self.tokenizer.advance()
        self.compileExpressionList()

        # Symbol: )
        self.subTag('symbol')
        self.tokenizer.advance()

    def compileDo(self):
        self.pointer = self.subTag('doStatement')

        # Keyword: Do
        self.subTag('keyword')
        self.tokenizer.advance()

        # Subroutine Call
        self.compileSubroutineCall()

        # Symbol: ;
        self.subTag('symbol')
        self.tokenizer.advance()

        self.pointer = self.pointer.getparent()

    def compileLet(self):

        self.pointer = self.subTag('letStatement')

        # Keyword: let
        self.subTag('keyword')
        self.tokenizer.advance()

        # identifier: varName
        self.subTagIdentifier(
            self.tokenizer.identifier(),
            self.symbolTable.kindOf(self.tokenizer.identifier()),
            'FALSE',
            self.symbolTable.kindOf(self.tokenizer.identifier()),
            self.symbolTable.indexOf(self.tokenizer.identifier())
        )
        self.tokenizer.advance()

        # index if applicable
        if self.tokenizer.symbol() == '[':
            
            # Symbol: [
            self.subTag('symbol')
            self.tokenizer.advance()

            # Expression
            self.compileExpression()

            # Symbol: ]
            self.subTag('symbol')
            self.tokenizer.advance()

        # Symbol: =
        self.subTag('symbol')
        self.tokenizer.advance()

        # Expression 
        self.compileExpression()

        # Symbol: ;
        self.subTag('symbol')
        self.tokenizer.advance()

        self.pointer = self.pointer.getparent()
    
    def compileWhile(self):

        self.pointer = self.subTag('whileStatement')

        # Keyword: while
        self.subTag('keyword')

        # Symbol: (
        self.tokenizer.advance()
        self.subTag('symbol')

        # Expression
        self.tokenizer.advance()
        self.compileExpression()

        # Symbol: )
        self.subTag('symbol')

        # Symbol: {
        self.tokenizer.advance()
        self.subTag('symbol')

        # Statements
        self.tokenizer.advance()
        self.compileStatements()

        # Symbol: }
        self.subTag('symbol')

        self.tokenizer.advance()

        self.pointer = self.pointer.getparent()

    def compileReturn(self):
        self.pointer = self.subTag('returnStatement')

        # Keyword: return
        self.subTag('keyword')

        # Symbol: ; or expression then ;
        self.tokenizer.advance()
        if self.tokenizer.token == ';':
            self.subTag('symbol')
        else:
            self.compileExpression()
            self.subTag('symbol')

        self.tokenizer.advance()

        self.pointer = self.pointer.getparent()

    def compileIf(self):
        self.pointer = self.subTag('ifStatement')

        # Keyword: if
        self.subTag('keyword')
        self.tokenizer.advance()

        # Symbol: (
        self.subTag('symbol')
        self.tokenizer.advance()

        # Expression
        self.compileExpression()

        # Symbol: )
        self.subTag('symbol')
        self.tokenizer.advance()

        # Symbol: {
        self.subTag('symbol')
        self.tokenizer.advance()

        # Statements
        self.compileStatements()

        # Symbol: }
        self.subTag('symbol')
        self.tokenizer.advance()

        if self.tokenizer.keyWord() == 'ELSE':

            # keyword: else
            self.subTag('keyword')

            # symbol: {
            self.tokenizer.advance()
            self.subTag('symbol')

            # Compile statements
            self.tokenizer.advance()
            self.compileStatements()

            # symbol: }
            self.subTag('symbol')
            
            self.tokenizer.advance()

        self.pointer = self.pointer.getparent()

    def compileExpression(self):
        self.pointer = self.subTag('expression')

        # Term
        self.compileTerm()

        while self.tokenizer.symbol() in CompilationEngine.op:

            # Symbol: op
            self.subTag('symbol')

            # Term
            self.tokenizer.advance()
            self.compileTerm()

        self.pointer = self.pointer.getparent()

    def compileTerm(self):
        self.pointer = self.subTag('term')

        tokenType = self.tokenizer.tokenType()

        if tokenType == 'INT_CONST':

            # Integer constant
            self.subTag('integerConstant')
            self.tokenizer.advance()

        elif tokenType == 'STRING_CONST':

            # String constant
            self.subTag('stringConstant')
            self.tokenizer.advance()

        elif tokenType == 'KEYWORD':

            # Keyword constant
            self.subTag('keyword')
            self.tokenizer.advance()

        elif tokenType == 'IDENTIFIER':
            # varName | varName[expression] | subroutineCall

            # Symbol: [ | ( | . 
            if self.tokenizer.lookAhead() == '[':
                # varName[expression]

                # Identifier: varName
                self.subTagIdentifier(
                    self.tokenizer.identifier(),
                    'VAR',
                    'FALSE',
                    self.symbolTable.kindOf(self.tokenizer.identifier()),
                    self.symbolTable.indexOf(self.tokenizer.identifier())
                )
                self.tokenizer.advance()

                # Symbol: [
                self.subTag('symbol')
                self.tokenizer.advance()

                # Expression
                self.compileExpression()

                # Symbol: ]
                self.subTag('symbol')
                self.tokenizer.advance()

            elif self.tokenizer.lookAhead() == '(' or self.tokenizer.lookAhead() == '.':
                # subroutine call
                self.compileSubroutineCall()

            else:
                # Identifier: varName
                self.subTagIdentifier(
                    self.tokenizer.identifier(),
                    'VAR',
                    'FALSE',
                    self.symbolTable.kindOf(self.tokenizer.identifier()),
                    self.symbolTable.indexOf(self.tokenizer.identifier())
                )
                self.tokenizer.advance()
            
        elif self.tokenizer.symbol() == '(':

            # ( Expression )

            # Symbol: (
            self.subTag('symbol')
            self.tokenizer.advance()

            # Expression
            self.compileExpression()
            
            # Symbol: )
            self.subTag('symbol')

            self.tokenizer.advance()

        elif self.tokenizer.symbol() in ['-', '~']:

            # Symbol: unaryop
            self.subTag('symbol')
            self.tokenizer.advance()

            # Term
            self.compileTerm()

        self.pointer = self.pointer.getparent()

    def compileExpressionList(self):
        self.pointer = self.subTag('expressionList')

        # Expression list may be empty, check
        if self.tokenizer.token is not ')':

            # Expression
            self.compileExpression()

            # Further comma delimited expressions
            while self.tokenizer.token == ',':
                self.subTag('symbol')
                self.tokenizer.advance()
                
                self.compileExpression()

        self.pointer = self.pointer.getparent()