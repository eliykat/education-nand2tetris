// Translation of ..\07\MemoryAccess\BasicTest\BasicTest.asm to ASM// Push constant 10 to stack
@10
D=A
@SP
A=M
M=D
@SP
M=M+1
// Pop value from stack to local[0]
@LCL
D=M
@0
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// Push constant 21 to stack
@21
D=A
@SP
A=M
M=D
@SP
M=M+1
// Push constant 22 to stack
@22
D=A
@SP
A=M
M=D
@SP
M=M+1
// Pop value from stack to argument[2]
@ARG
D=M
@2
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// Pop value from stack to argument[1]
@ARG
D=M
@1
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// Push constant 36 to stack
@36
D=A
@SP
A=M
M=D
@SP
M=M+1
// Pop value from stack to this[6]
@THIS
D=M
@6
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// Push constant 42 to stack
@42
D=A
@SP
A=M
M=D
@SP
M=M+1
// Push constant 45 to stack
@45
D=A
@SP
A=M
M=D
@SP
M=M+1
// Pop value from stack to that[5]
@THAT
D=M
@5
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// Pop value from stack to that[2]
@THAT
D=M
@2
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// Push constant 510 to stack
@510
D=A
@SP
A=M
M=D
@SP
M=M+1
// Pop value from stack to temp[6]
@5
D=A
@6
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// Push value to stack from local[0]
@LCL
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// Push value to stack from that[5]
@THAT
D=M
@5
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// Add
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=D+M
M=D
// Push value to stack from argument[1]
@ARG
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// Subtract
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=M-D
M=D
// Push value to stack from this[6]
@THIS
D=M
@6
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// Push value to stack from this[6]
@THIS
D=M
@6
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// Add
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=D+M
M=D
// Subtract
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=M-D
M=D
// Push value to stack from temp[6]
@5
D=A
@6
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// Add
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=D+M
M=D
// End loop
(END)
@END
0;JMP