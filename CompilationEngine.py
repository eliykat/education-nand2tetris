from JackTokenizer import JackTokenizer
from TokenTypeError import TokenTypeError
from SymbolTable import SymbolTable
from VMWriter import VMWriter
import sys

class CompilationEngine():

    op = ['+', '-', '*', '/', '&', '|', '<', '>', '=']

    def __init__(self, input, output):
        self.input = input

        # Instantiate different modules
        self.tokenizer = JackTokenizer(input)
        self.symbolTable = SymbolTable()
        self.vmWriter = VMWriter(output)

        # Unique number - used for labels
        self.uniqueNo = -1

        # Load up the first token
        self.tokenizer.advance()

        # Call compileClass to start the compilation
        self.compileClass()

    def subTag(self, _tag):
        print('Subtag encountered - fix this')
        raise NameError
        sys.exit()

    def subTagIdentifier(self, name, category, new, kind, index):
        print('Subtag encountered - fix this')
        raise NameError
        sys.exit()

    def getUniqueNo(self):
        self.uniqueNo += 1
        return str(self.uniqueNo)
    
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
        while not self.tokenizer.rawToken() == '}':      # Access token directly to circumvent error checking
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
        self.tokenizer.advance()

        # Keyword: void | type | identifier (if class)
        self.tokenizer.advance()

        # Identifier: subroutineName
        subroutineName = self.tokenizer.identifier()
        self.tokenizer.advance()

        # Symbol: (
        self.tokenizer.advance()

        # Program structure: ParameterList
        self.compileParameterList()

        # Symbol: )
        self.tokenizer.advance()

        ### START SUBROUTINE BODY ###

        # Symbol: {
        self.tokenizer.advance()

        # subroutineBody: varDecs
        while self.tokenizer.keyWord() == 'VAR':
            self.compileVarDec()

        # Write vm code function declaration
        # This is done 'late' so that we can get nLocals (noting that varDec() does not actually write vm code)
        self.vmWriter.writeFunction(self.className + '.' + subroutineName, self.symbolTable.varCount('LOCAL'))
        
        # subroutineBody: Statements
        self.compileStatements()

        # Symbol: }
        self.tokenizer.advance()

        ### END SUBROUTINE BODY ###

    def compileParameterList(self):
        # assume pointer is on keyword: type of first parameter OR symbol: ( if no parameters

        if self.tokenizer.rawToken() is not ')':
            run_once = True
            while self.tokenizer.rawToken() == ',' or run_once == True:

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
                    'ARGUMENT'
                )
                self.tokenizer.advance()

                run_once = False

    def compileVarDec(self):
        # assume pointer is on keyword: var

        # Keyword: var
        self.tokenizer.advance()

        # Keyword: type | identifier (if class)
        try:
            _type = self.tokenizer.keyWord()
        except TokenTypeError:
            _type = self.tokenizer.identifier()
        finally:
            self.tokenizer.advance()

        # Identifier: varName
        # Define in symboltable - note that no actual VM code is required here
        self.symbolTable.define(
            self.tokenizer.identifier(),
            _type,
            'LOCAL')
        self.tokenizer.advance()

        # Further varNames
        while self.tokenizer.symbol() == ',':
            # Symbol: ,
            self.tokenizer.advance()
            
            # Identifier: varName
            self.symbolTable.define(
                self.tokenizer.identifier(),
                _type,
                'LOCAL')
            self.tokenizer.advance()

        # Symbol: ;
        self.tokenizer.advance()

    def compileStatements(self):
        # assume token is keyword: let | if | while | do | return

        # note: each of the nested compile methods call tokenizer.advance() at the end,
        # so no need to call it here

        while self.tokenizer.rawToken() is not '}':
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
                raise TokenTypeError('Statement keyword', self.tokenizer.tokenType(), self.tokenizer.rawToken(), self.tokenizer.lineNo)

    def compileSubroutineCall(self):
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

        # Write function call
        self.vmWriter.writeCall(subroutineName, nArgs)

    def compileDo(self):

        # Keyword: Do
        self.tokenizer.advance()

        self.compileSubroutineCall()
        
        # Symbol: ;
        self.tokenizer.advance()

    def compileLet(self):

        # Keyword: let
        self.tokenizer.advance()

        # identifier: varName
        varName = self.tokenizer.identifier()
        self.tokenizer.advance()

        # index if applicable
        if self.tokenizer.symbol() == '[':
            
            # Symbol: [
            self.tokenizer.advance()

            # Expression
            self.compileExpression()

            # Symbol: ]
            self.tokenizer.advance()

        # Symbol: =
        self.tokenizer.advance()

        # Expression 
        self.compileExpression()

        # Symbol: ;
        self.tokenizer.advance()

        # Write VM code - pop from top of stack to variable
        self.vmWriter.writePop(
            self.symbolTable.kindOf(varName),
            self.symbolTable.indexOf(varName)
        )
    
    def compileWhile(self):

        # Get a new unique number
        uniqueNo = self.getUniqueNo()

        # Keyword: while
        self.tokenizer.advance()

        # Symbol: (
        self.tokenizer.advance()

        # startWhile label
        self.vmWriter.writeLabel('startWhile' + uniqueNo)
        
        # Expression
        self.compileExpression()

        # Jump if expression is FALSE
        # (Pushing constant 1 and adding has the effect of inverting the truthiness of the test value)
        self.vmWriter.writePush('constant', 1)
        self.vmWriter.writeArithmetic('ADD')
        self.vmWriter.writeIf('endWhile' + uniqueNo)

        # Symbol: )
        self.tokenizer.advance()

        # Symbol: {
        self.tokenizer.advance()

        # Statements
        self.compileStatements()

        # Jump to startWhile
        self.vmWriter.writeGoto('startWhile' + uniqueNo)

        # endWhile label
        self.vmWriter.writeLabel('endWhile' + uniqueNo)

        # Symbol: }
        self.tokenizer.advance()

    def compileReturn(self):

        # Keyword: return
        self.tokenizer.advance()

        # Symbol: ; or expression then ;
        if self.tokenizer.rawToken() is not ';':
            self.compileExpression()

        self.tokenizer.advance()

        # Write return
        self.vmWriter.writeReturn()

    def compileIf(self):

        # Get new unique no
        uniqueNo = self.getUniqueNo()

        # Keyword: if
        self.tokenizer.advance()

        # Symbol: (
        self.tokenizer.advance()

        # Expression
        self.compileExpression()

        # Jump if expression is FALSE
        # (Pushing constant 1 and adding has the effect of inverting the truthiness of the test value)
        self.vmWriter.writePush('constant', 1)
        self.vmWriter.writeArithmetic('ADD')
        self.vmWriter.writeIf('startElse' + uniqueNo)

        # Symbol: )
        self.tokenizer.advance()

        # Symbol: {
        self.tokenizer.advance()

        # Statements
        self.compileStatements()

        # Symbol: }
        self.tokenizer.advance()

        self.vmWriter.writeGoto('endIf' + uniqueNo)

        self.vmWriter.writeLabel('startElse' + uniqueNo)

        if self.tokenizer.keyWord() == 'ELSE':

            # keyword: else
            self.tokenizer.advance()

            # symbol: {
            self.tokenizer.advance()
            
            # Compile statements
            self.compileStatements()

            # symbol: }
            self.tokenizer.advance()

        self.vmWriter.writeLabel('endIf' + uniqueNo)

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

            # Keyword constant (true | false | null | this)     ########## NB: LET LOOP = TRUE; IS NOT PUSHING -1 TO STACK
            if self.tokenizer.keyWord() == 'TRUE':
                self.vmWriter.writePush('constant', 1)
                self.vmWriter.writeArithmetic('NEG')

            elif self.tokenizer.keyWord() == 'FALSE' or self.tokenizer.keyWord() == 'NULL':
                self.vmWriter.writePush('constant', 0)

            elif self.tokenizer.keyWord() == 'THIS':
                self.vmWriter.writePush('pointer', 0)

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
                # Retrieve segment and index from symboltable and push to top of stack
                self.vmWriter.writePush(
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
            op = self.tokenizer.symbol()
            self.tokenizer.advance()

            # Term
            self.compileTerm()

            # Write op
            if op == '-':
                self.vmWriter.writeArithmetic('NEG')
            elif op == '~':
                self.vmWriter.writeArithmetic('NOT')

    def compileExpressionList(self):
        
        nArgs = 0

        # Expression list may be empty, check
        if self.tokenizer.rawToken() is not ')':

            # Expression
            self.compileExpression()
            nArgs += 1

            # Further comma delimited expressions
            while self.tokenizer.rawToken() == ',':
                # Symbol: ,
                self.tokenizer.advance()
                
                # Expression
                self.compileExpression()
                nArgs += 1

        return nArgs