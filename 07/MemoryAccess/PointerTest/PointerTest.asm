// Translation of ..\07\MemoryAccess\PointerTest\PointerTest.asm to ASM 
// Push constant 3030 to stack
@3030
D=A
@SP
A=M
M=D
@SP
M=M+1
// Pop value from stack to pointer[0]
@3
D=A
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
// Push constant 3040 to stack
@3040
D=A
@SP
A=M
M=D
@SP
M=M+1
// Pop value from stack to pointer[1]
@3
D=A
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
// Push constant 32 to stack
@32
D=A
@SP
A=M
M=D
@SP
M=M+1
// Pop value from stack to this[2]
@THIS
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
// Push constant 46 to stack
@46
D=A
@SP
A=M
M=D
@SP
M=M+1
// Pop value from stack to that[6]
@THAT
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
// Push value to stack from pointer[0]
@3
D=A
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// Push value to stack from pointer[1]
@3
D=A
@1
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
// Push value to stack from this[2]
@THIS
D=M
@2
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
// Push value to stack from that[6]
@THAT
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
// End loop
(END)
@END
0;JMP
