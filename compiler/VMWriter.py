class SegmentError(Exception):
    def __init__(self, segment):
        self.segment = segment

class VMWriter:

    segments = [
        'argument',
        'local',
        'static',
        'constant',
        'this',
        'that',
        'pointer',
        'temp'
    ]

    def __init__(self, output):
        self.output = open(output, 'w')
        self.debug = True

    def writePush(self, segment, index):
        if segment not in VMWriter.segments:
            raise SegmentError(segment)

        self.output.write('push ' + segment + ' ' + str(index) + '\n')
        if self.debug: print('push ' + segment + ' ' + str(index) + '\n')

    def writePop(self, segment, index):
        if segment not in VMWriter.segments:
            raise SegmentError(segment)

        self.output.write('pop ' + segment + ' ' + str(index) + '\n')
        if self.debug: print('pop ' + segment + ' ' + str(index) + '\n')

    def writeArithmetic(self, command):
        self.output.write(command.lower() + '\n')
        if self.debug: print(command.lower() + '\n')

    def writeLabel(self, label):
        self.output.write('label ' + label + '\n')
        if self.debug: print('label ' + label + '\n')

    def writeGoto(self, label):
        self.output.write('goto ' + label + '\n')
        if self.debug: print('goto ' + label + '\n')

    def writeIf(self, label):
        self.output.write('if-goto ' + label + '\n')
        if self.debug: print('if-goto ' + label + '\n')

    def writeCall(self, name, nArgs):
        self.output.write('call ' + name + ' ' + str(nArgs) + '\n')
        if self.debug: print('call ' + name + ' ' + str(nArgs) + '\n')

    def writeFunction(self, name, nLocals):
        self.output.write('function ' + name + ' ' + str(nLocals) + '\n')
        if self.debug: print('function ' + name + ' ' + str(nLocals) + '\n')

    def writeReturn(self):
        self.output.write('return\n')
        if self.debug: print('return\n')

    def close(self):
        self.output.close()