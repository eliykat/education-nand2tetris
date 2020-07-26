// INITIALIZE VM
@256
D=A
@SP
M=D
// CALL FUNCTION Sys.init
// Push constant Sys.init0.return to stack
@Sys.init0.return
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(Sys.init0.return)
// TERMINATE PROGRAM (sys.init should do this, but just in case)
(END)
@END
0;JMP
// ----------------------------------------------------
// COMMENCE FILE: ..\08\FunctionCalls\FibonacciElement\
// ----------------------------------------------------
// DECLARING FUNCTION Main.fibonacci
(Main.fibonacci)
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
// Push constant 2 to stack
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// Less than
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=M-D
@TRUE.1
D;JLT
@SP
A=M-1
M=0
@END.1
0;JMP
(TRUE.1)
@SP
A=M-1
M=-1
(END.1)
@SP
M=M-1
A=M
D=M
@FibonacciElement.Main.fibonacci_IF_TRUE
D;JNE
@FibonacciElement.Main.fibonacci_IF_FALSE
0;JMP
(FibonacciElement.Main.fibonacci_IF_TRUE)
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
// RETURN FROM FUNCTION Main.fibonacci
@LCL
D=M
@FRAME1
M=D
@5
A=D-A
D=M
@RET1
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
@ARG
D=M+1
@SP
M=D
@FRAME1
A=M-1
D=M
@THAT
M=D
@FRAME1
A=M-1
A=A-1
D=M
@THIS
M=D
@FRAME1
A=M-1
A=A-1
A=A-1
D=M
@ARG
M=D
@FRAME1
A=M-1
A=A-1
A=A-1
A=A-1
D=M
@LCL
M=D
@RET1
A=M
0;JMP
(FibonacciElement.Main.fibonacci_IF_FALSE)
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
// Push constant 2 to stack
@2
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
// CALL FUNCTION Main.fibonacci
// Push constant Main.fibonacci2.return to stack
@Main.fibonacci2.return
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@6
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci2.return)
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
// CALL FUNCTION Main.fibonacci
// Push constant Main.fibonacci3.return to stack
@Main.fibonacci3.return
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@6
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci3.return)
// Add
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=D+M
M=D
// RETURN FROM FUNCTION Main.fibonacci
@LCL
D=M
@FRAME4
M=D
@5
A=D-A
D=M
@RET4
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
@ARG
D=M+1
@SP
M=D
@FRAME4
A=M-1
D=M
@THAT
M=D
@FRAME4
A=M-1
A=A-1
D=M
@THIS
M=D
@FRAME4
A=M-1
A=A-1
A=A-1
D=M
@ARG
M=D
@FRAME4
A=M-1
A=A-1
A=A-1
A=A-1
D=M
@LCL
M=D
@RET4
A=M
0;JMP
// ----------------------------------------------------
// COMMENCE FILE: ..\08\FunctionCalls\FibonacciElement\
// ----------------------------------------------------
// DECLARING FUNCTION Sys.init
(Sys.init)
// Push constant 4 to stack
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
// CALL FUNCTION Main.fibonacci
// Push constant Main.fibonacci4.return to stack
@Main.fibonacci4.return
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@6
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci4.return)
(FibonacciElement.Sys.init_WHILE)
@FibonacciElement.Sys.init_WHILE
0;JMP