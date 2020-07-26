(BLACKOUT)

    // Reset next screen pixel to start of the SCREEN range
    @SCREEN
    D=A
    @NEXT
    M=D

    (BLOOP)
        // Jump to WHITEOUT if a key is not pressed
        @KBD
        D=M
        @WHITEOUT
        D;JEQ
        
        // Check if the screen is already black - if so, just loop key detection without doing anything further
        @NEXT
        D=M
        @24576  // this is the upper bound of the screen section of memory
        D=A-D
        @BLOOP
        D;JLE

        // Black out the next pixel
        @0
        D=!A
        @NEXT
        A=M
        M=D
        
        // move the pointer up by 1
        @NEXT
        M=M+1
        
        @BLOOP
        0;JMP

(WHITEOUT)

    // Reset next screen pixel to start of the SCREEN range
    @SCREEN
    D=A
    @NEXT
    M=D

    (WLOOP)
        // Jump to BLACKOUT if a key is pressed
        @KBD
        D=M
        @BLACKOUT
        D;JGT
        
        // Check if the screen is already white - if so, just loop key detection without doing anything further
        @NEXT
        D=M
        @24576  // this is the upper bound of the screen section of memory
        D=A-D
        @BLOOP
        D;JLE

        // White out the next pixel
        @0
        D=A
        @NEXT
        A=M
        M=D
        
        // move the pointer up by 1
        @NEXT
        M=M+1
        
        @WLOOP
        0;JMP