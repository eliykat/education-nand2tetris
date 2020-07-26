// set R2 to 0 on first run
@0
D=A
@R2
M=D

(LOOP)

    // test if R1 > 0. Done at start so that no operations are done if R1 is set to 0 from the start.
    @R1
    D=M
    @END
    D;JEQ   //jump to the end of the loop if the R1 == 0

    // If we're still here, then we need to execute the next addition
    // add R0 to R2
    @R0  
    D=M     // Load R0 and store in D
    @R2    // Load R2
    M=D+M   // add D and M registers and store value in M
    
    // Subtract 1 from the count
    @R1
    M=M-1
    
    @LOOP
    0;JMP

(END)
    // terminate execution
    @END
    0;JMP