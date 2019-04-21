class SymbolTable:

    def __init__(self):
        # Initialise new class scope symbol table
        self.classScope = {}

        # Initialise new dict used to keep track of index counts
        self.indexCount = {
            'STATIC': 0,
            'FIELD': 0,
            'ARG': 0,
            'VAR': 0
        }

    def startSubroutine(self):
        # Initialise new subroutine scope symbol table
        # Implicitly destroys the existing one
        self.subroutineScope = {}

        # Reset indexCount for subroutine scoped variables
        self.indexCount['ARG'] = 0
        self.indexCount['VAR'] = 0

    def define(self, _name, _type, _kind):
        if _kind == 'STATIC' or _kind == 'FIELD':
            # Class scope
            scope = self.classScope

        elif _kind == 'ARG' or _kind == 'VAR':
            # Subroutine scope
            scope = self.subroutineScope

        scope[_name] = {
            'name': _name,      # Identifier
            'type': _type,      # boolean, int, className
            'kind': _kind,      # STATIC, FIELD, VAR, ARG
            'index': self.indexCount[_kind]     # Unique index per kind
        }

        self.indexCount[_kind] += 1

    def varCount(self, _kind):
        return self.indexCount[_kind]

    def kindOf(self, _name):
        try:
            if _name in self.subroutineScope:
                return self.subroutineScope[_name]['kind']
        except AttributeError:
            pass
        
        if _name in self.classScope:
            return self.classScope[_name]['kind']

        else:
            return 'NONE'

    def typeOf(self, _name):
        try:
            if _name in self.subroutineScope:
                return self.subroutineScope[_name]['type']
        except AttributeError:
            pass

        if _name in self.classScope:
            return self.classScope[_name]['type']

        else:
            return 'NONE'

    def indexOf(self, _name):
        try:
            if _name in self.subroutineScope:
                return self.subroutineScope[_name]['index']
        except AttributeError:
            pass
        
        if _name in self.classScope:
            return self.classScope[_name]['index']

        else:
            return 'NONE'