from JackTokenizer import JackTokenizer
from lxml import etree

class CompilationEngine():

    def __init__(self, input, output):
        self.input = input
        self.output = open(output, 'w')
        self.tokenizer = JackTokenizer(input)

        self.tokenizer.advance()

        self.root = etree.Element('root')
        self.pointer = self.root

        # Compile the class (should not be any other token)
        self.compileClass()

    def subTag(self, _tag):
        result = etree.SubElement(self.pointer, _tag)

        if _tag == 'keyword':
            result.text = self.tokenizer.keyWord()
        elif _tag == 'symbol':
            result.text = self.tokenizer.symbol()
        elif _tag == 'identifier':
            result.text = self.tokenizer.identifier()
        elif _tag == 'int_const':
            result.text = self.tokenizer.intVal()
        elif _tag == 'string_const':
            result.text = self.tokenizer.stringVal()

        return result
    
    def compileClass(self):
        # Current token assumed to be the CLASS keyword
    
        # Class XML tag and move pointer
        self.pointer = self.subTag('class')

        # Keyword: class
        self.subTag('keyword')

        # Identifier: class name
        self.tokenizer.advance()
        self.subTag('identifier')

        # Symbol: {
        self.tokenizer.advance()
        self.subTag('symbol')

        # classVarDec or Subroutine
        while not self.tokenizer.token == '}':      # Access token directly to circumvent error checking
            self.tokenizer.advance()
            if self.tokenizer.keyWord() in ['STATIC', 'FIELD']:
                self.compileClassVarDec()
            elif self.tokenizer.keyWord() in ['CONSTRUCTOR', 'FUNCTION', 'METHOD', 'VOID', 'INT', 'CHAR', 'BOOLEAN']:
                self.compileSubroutine()

        # Symbol: }
        self.subTag('symbol')

        # Move pointer up to parent
        self.pointer = self.pointer.getparent()

        # Move to the next token (which should only be a class declaration) if available, otherwise finish compilation
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.compileClass()
        else:
            self.close()

    def close(self):
        self.tokenizer.close()

        ## Write to output file and close
        self.output.write(etree.tostring(self.root, pretty_print=True))
        self.output.close()
        self.tokenizer.close()

        print('CompilationEngine complete.')
    
    def compileClassVarDec(self):
        # Current token assumed to be the STATIC or FIELD keyword

        # Create XML tag and move pointer
        self.pointer = self.subTag('classVarDec')

        # Keyword: STATIC or FIELD
        self.subTag('keyword')

        # Keyword: type
        self.tokenizer.advance()
        self.subTag('keyword')

        # Identifier: varName
        self.tokenizer.advance()
        self.subTag('identifier')

        # Compile any other varDecs on the same line (of the same type)
        self.tokenizer.advance()
        while self.tokenizer.symbol() == ',':
            self.subTag('symbol')
            self.tokenizer.advance()
            self.subTag('identifier')
            self.tokenizer.advance()

        # Symbol: ;
        self.subTag('symbol')

        self.tokenizer.advance()

        # Move pointer back up
        self.pointer = self.pointer.getparent()       

    def compileSubroutine(self):
        # Current token assumed to be keyword: constructor | function | method | void | <type>
    
        # Create XML element and move pointer
        self.pointer = self.subTag('subroutineDec')

        # Keyword: constructor | function | method | void | <type>
        self.subTag('keyword')

        # Identifier: subroutineName
        self.tokenizer.advance()
        self.subTag('identifier')

        # Symbol: (
        self.tokenizer.advance()
        self.subTag('symbol')

        # Program structure: ParameterList
        self.tokenizer.advance()
        self.compileParameterList()

        # Symbol: )
        self.subTag('symbol')

        # Symbol: {
        self.tokenizer.advance()
        self.subTag('symbol')

        # subroutineBody: varDecs
        self.tokenizer.advance()
        while self.tokenizer.keyWord() == 'var':
            self.compileVarDec()
        
        # subroutineBody: Statements
        self.compileStatements()

        # Symbol: }
        self.subTag('symbol')

        self.tokenizer.advance()

        # Move pointer up
        self.pointer = self.pointer.getparent()

    def compileParameterList(self):
        # assume pointer is on keyword: type of first parameter OR symbol: ( if no parameters

        # Create XML tree and descend into it
        self.pointer = self.subTag('parameterList')

        if self.tokenizer.token is not ')':
            run_once = True
            while self.tokenizer.symbol() == ',' or run_once == True:

                if run_once == False:
                    # Symbol: ,
                    self.subTag('symbol')
                
                # Keyword: type
                self.subTag('keyword')

                # Identifier: varName
                self.tokenizer.advance()
                self.subTag('identifier')
                
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

        # Keyword: <type>
        self.tokenizer.advance()
        self.subTag('keyword')

        # Identifier: varName
        self.tokenizer.advance()
        self.subTag('identifier')

        self.tokenizer.advance()

        # Further varNames
        while self.tokenizer.symbol() == ',':
            self.subTag('symbol')
            self.tokenizer.advance()
            self.subTag('identifier')
            self.tokenizer.advance()

        # Symbol: ;
        self.subTag('symbol')

        self.tokenizer.advance()

        # Ascend
        self.pointer.getparent()

    def compileStatements(self):
        # assume token is keyword: let | if | while | do | return

        # create XML tree and descend
        self.pointer = self.subTag('Statements')

        # note: each of the nested compile methods call tokenizer.advance() at the end,
        # so no need to call it here

        while self.tokenizer.token is not '}':
            if self.tokenizer.keyWord() == 'let':
                self.compileLet()
            elif self.tokenizer.keyWord() == 'if':
                self.compileIf()
            elif self.tokenizer.keyWord() == 'while':
                self.compileWhile()
            elif self.tokenizer.keyWord() == 'do':
                self.compileDo()
            elif self.tokenizer.keyWord() == 'return':
                self.compileReturn()

        self.pointer = self.pointer.getparent()

    def compileDo(self):
        pass

    def compileLet(self):

        self.pointer = self.subTag('letStatement')

        # TEMPORARY: PASS OVER
        while self.tokenizer.token is not ';':
            self.tokenizer.advance()

        self.tokenizer.advance()

        self.pointer = self.pointer.getparent()
    
    def compileWhile(self):

        self.pointer = self.subTag('whileStatement')

        # TEMPORARY: PASS OVER
        while self.tokenizer.token is not '{':
            self.tokenizer.advance()

        self.tokenizer.advance()

        # Call statements
        self.compileStatements()

        self.tokenizer.advance()

        self.pointer = self.pointer.getparent()

    def compileReturn(self):
        self.pointer = self.subTag('returnStatement')

        # TEMPORARY: PASS OVER
        while self.tokenizer.token is not ';':
            self.tokenizer.advance()

        self.tokenizer.advance()

        self.pointer = self.pointer.getparent()

    def compileIf(self):
        self.pointer = self.subTag('ifStatement')

        # TEMPORARY: PASS OVER
        while self.tokenizer.token is not '{':
            self.tokenizer.advance()

        self.tokenizer.advance()

        # Call statements
        self.compileStatements()

        self.tokenizer.advance()

        if self.tokenizer.token == 'else':

            # keyword: else
            self.subTag('keyword')

            # symbol: {
            self.tokenizer.advance()
            self.subTag('symbol')

            # Compile statements
            self.compileStatements()

            # symbol: }
            self.subTag('symbol')
            
            self.tokenizer.advance()

        self.pointer = self.pointer.getparent()

    def compileExpression(self):
        pass

    def compileTerm(self):
        pass

    def compileExpressionList(self):
        pass