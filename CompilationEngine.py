from JackTokenizer import JackTokenizer
from TokenTypeError import TokenTypeError
from SymbolTable import SymbolTable
from VMWriter import VMWriter
import sys

class CompilationEngine():

    op = ['+', '-', '*', '/', '&', '|', '<', '>', '=']

    def __init__(self, input, output):
        self.input = input

        self.tokenizer = JackTokenizer(input)
        self.symbolTable = SymbolTable()
        self.vmWriter = VMWriter(output)

        self.tokenizer.advance()

        # Compile the class (should not be any other token)
        self.compileClass()

    def subTag(self, _tag):
        print('Subtag encountered - fix this')
        raise NameError
        sys.exit()

    def subTagIdentifier(self, name, category, new, kind, index):
        print('Subtag encountered - fix this')
        raise NameError
        sys.exit()
    
    def compileClass(self):
        # Current token assumed to be the CLASS keyword

        # Keyword: class
        self.tokenizer.advance()

        # Identifier: class name
        # Classes are not entered into symboltable
        self.className = self.tokenizer.identifier()
        self.tokenizer.advance()

        # Symbol: {
        self.tokenizer.advance()

        # classVarDec or Subroutine
        while not self.tokenizer.token == '}':      # Access token directly to circumvent error checking
            if self.tokenizer.keyWord() in ['STATIC', 'FIELD']:
                self.compileClassVarDec()
            elif self.tokenizer.keyWord() in ['CONSTRUCTOR', 'FUNCTION', 'METHOD']:
                self.compileSubroutine()

        # Symbol: }
        # Do not advance, we are done

        self.close()

    def close(self):
        self.vmWriter.close()
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

        # Keyword: constructor | function | method 
        subroutineType = self.tokenizer.keyWord()
        self.tokenizer.advance()

        # Keyword: void | type | identifier (if class)
        try:
            # Void | type
            returnType = self.tokenizer.keyWord()
        except TokenTypeError:
            # Identifier: class
            returnType = self.tokenizer.identifier()
        self.tokenizer.advance()

        # Identifier: subroutineName
        subroutineName = self.tokenizer.identifier()
        self.tokenizer.advance()

        # Symbol: (
        self.tokenizer.advance()

        # Program structure: ParameterList
        nLocals = self.compileParameterList()

        # Symbol: )
        self.tokenizer.advance()

        # Write function dec
        self.vmWriter.writeFunction(self.className + '.' + subroutineName, nLocals)

        ### START SUBROUTINE BODY ###

        # Symbol: {
        self.tokenizer.advance()

        # subroutineBody: varDecs
        while self.tokenizer.keyWord() == 'VAR':
            self.compileVarDec()
        
        # subroutineBody: Statements
        self.compileStatements()

        # Symbol: }
        self.tokenizer.advance()

        ### END SUBROUTINE BODY ###

    def compileParameterList(self):
        # assume pointer is on keyword: type of first parameter OR symbol: ( if no parameters

        nLocals = 0

        if self.tokenizer.token is not ')':
            run_once = True
            while self.tokenizer.token == ',' or run_once == True:

                if run_once == False:
                    # Symbol: ,
                    self.tokenizer.advance()
                
                # Keyword: type
                _type = self.tokenizer.keyWord()
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
                nLocals += 1
                self.tokenizer.advance()

                run_once = False

        # Return number of arguments
        return nLocals

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

    def compileDo(self):

        # Keyword: Do
        self.tokenizer.advance()

        # Identifier: subroutineName or (className | varName)
        subroutineName = self.tokenizer.identifier()
        self.tokenizer.advance()

        # Symbol: . (indicating format of className.subroutineName) or ( (indicating format of subroutineName)
        if self.tokenizer.symbol() == ".":
            subroutineName += self.tokenizer.symbol()
            self.tokenizer.advance()

            # Identifier: subroutineName
            subroutineName += self.tokenizer.identifier()
            self.tokenizer.advance()

            # Symbol: (
            self.tokenizer.advance()

        nArgs = self.compileExpressionList()

        # Symbol: )
        self.tokenizer.advance()

        # Symbol: ;
        self.tokenizer.advance()

        # Write function call
        self.vmWriter.writeCall(subroutineName, nArgs)

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

        # Keyword: return
        self.tokenizer.advance()

        # Symbol: ; or expression then ;
        if self.tokenizer.token is not ';':
            self.compileExpression()

        self.tokenizer.advance()

        # Write return
        self.vmWriter.writeReturn()

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
        # Term
        self.compileTerm()

        while self.tokenizer.symbol() in CompilationEngine.op:

            # Symbol: op
            # Save for writing later
            op = self.tokenizer.symbol()
            self.tokenizer.advance()

            # Term
            self.compileTerm()

            # Write op
            if op == '+':
                self.vmWriter.writeArithmetic('ADD')
            elif op == '-':
                self.vmWriter.writeArithmetic('SUB')
            elif op == '=':
                self.vmWriter.writeArithmetic('EQ')
            elif op == '>':
                self.vmWriter.writeArithmetic('GT')
            elif op == '<':
                self.vmWriter.writeArithmetic('LT')
            elif op == '&':
                self.vmWriter.writeArithmetic('AND')
            elif op == '|':
                self.vmWriter.writeArithmetic('OR')
            elif op == '~':
                self.vmWriter.writeArithmetic('NOT')
            elif op == '*':
                self.vmWriter.writeCall('Math.multiply', 2)

    def compileTerm(self):

        tokenType = self.tokenizer.tokenType()

        if tokenType == 'INT_CONST':

            # Integer constant
            self.vmWriter.writePush('constant', self.tokenizer.intVal())
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
                self.compileDo()

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
            self.tokenizer.advance()

            # Expression
            self.compileExpression()
            
            # Symbol: )
            self.tokenizer.advance()

        elif self.tokenizer.symbol() in ['-', '~']:

            # Symbol: unaryop
            self.subTag('symbol')
            self.tokenizer.advance()

            # Term
            self.compileTerm()

    def compileExpressionList(self):
        
        nArgs = 0

        # Expression list may be empty, check
        if self.tokenizer.token is not ')':

            # Expression
            self.compileExpression()
            nArgs += 1

            # Further comma delimited expressions
            while self.tokenizer.token == ',':
                # Symbol: ,
                self.tokenizer.advance()
                
                self.compileExpression()
                nArgs += 1

        return nArgs