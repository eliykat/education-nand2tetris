// Translation of ..\07\MemoryAccess\StaticTest\StaticTest.asm to ASM 
// Push constant 111 to stack
@111
D=A
@SP
A=M
M=D
@SP
M=M+1
// Push constant 333 to stack
@333
D=A
@SP
A=M
M=D
@SP
M=M+1
// Push constant 888 to stack
@888
D=A
@SP
A=M
M=D
@SP
M=M+1
// Pop value from stack to static[8]
@StaticTest.8
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// Pop value from stack to static[3]
@StaticTest.3
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// Pop value from stack to static[1]
@StaticTest.1
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// Push value to stack from static[3]
@StaticTest.3
D=M
@SP
A=M
M=D
@SP
M=M+1
// Push value to stack from static[1]
@StaticTest.1
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
// Push value to stack from static[8]
@StaticTest.8
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
