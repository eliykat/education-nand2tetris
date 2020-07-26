// Translation of ..\08\ProgramFlow\BasicLoop\BasicLoop.asm to ASM 
// Push constant 0 to stack
@0
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
(LOOP_START)
// Push value to stack from argument[0]
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
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
// Add
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=D+M
M=D
// Pop value from stack to local[0	]
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
// Push value to stack from argument[0]
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// Push constant 1 to stack
@1
D=A
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
// Pop value from stack to argument[0]
@ARG
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
// Push value to stack from argument[0]
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@LOOP_START
D;JNE
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
// End loop
(END)
@END
0;JMP
