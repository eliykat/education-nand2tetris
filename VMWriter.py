class VMWriter:

    def __init__(self, output):
        self.output = open(output, 'w')

    def writePush(self, segment, index):
        self.output.write('push ' + segment + ' ' + str(index) + '\n')

    def writePop(self, segment, index):
        self.output.write('pop ' + segment + ' ' + str(index) + '\n')

    def writeArithmetic(self, command):
        self.output.write(command.lower() + '\n')

    def writeLabel(self, label):
        self.output.write('label ' + label + '\n')

    def writeGoto(self, label):
        self.output.write('goto ' + label + '\n')

    def writeIf(self, label):
        self.output.write('if-goto ' + label + '\n')

    def writeCall(self, name, nArgs):
        self.output.write('call ' + name + ' ' + str(nArgs) + '\n')

    def writeFunction(self, name, nLocals):
        self.output.write('function ' + name + ' ' + str(nLocals) + '\n')

    def writeReturn(self):
        self.output.write('return\n')

    def close(self):
        self.output.close()