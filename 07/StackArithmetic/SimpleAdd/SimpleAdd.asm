// Push constant 7 to stack
@7
D=A
@SP
A=M
M=D
@SP
M=M+1
// Push constant 8 to stack
@8
D=A
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
@END
(END)
0;JMP
