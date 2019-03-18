const fs = require('fs');

export class CodeWriter {

    output: string;
    counter: number = 0;

    setFileName(filename: string){

    }

    writeArithmetic(command: string) {
        
        // Increment the unique counter by 1,
        // regardless of which type of command it is
        this.counter += 1;

        switch(command) {

            case "add": {
                this.writeToFile([
                    "// Add",
                    "@SP",
                    "M=M-1",    // Decrement SP by 1
                    "A=M",
                    "D=M",      // Load top value into D
                    "@SP",
                    "A=M-1",    // Point A to second-to-top value
                    "D=D+M",    // Perform the addition
                    "M=D"       // Store the result at the top of the stack
                ])
                break;
            }

            case "sub": {
                this.writeToFile([
                    "// Subtract",
                    "@SP",
                    "M=M-1",    // Decrement SP by 1
                    "A=M",
                    "D=M",      // Load top value into D
                    "@SP",
                    "A=M-1",    // Point A to second-to-top value
                    "D=M-D",    // Perform the subtraction
                    "M=D"       // Store the result at the top of the stack
                ])
                break;
            }

            case "neg": {
                this.writeToFile([
                    "// Negation",
                    "@SP",
                    "A=M-1",      // Get the last value on the stack
                    "M=-M",       // Perform the negation and store it
                    // No need to change stack pointer
                ])
                break;
            }

            case "eq": {
                this.writeToFile([
                    "// Eq",
                    "@SP",
                    "M=M-1",    // Decrement SP by 1
                    "A=M",
                    "D=M",      // Load top value into D
                    "@SP",
                    "A=M-1",    // Point A to second-to-top value
                    "D=M-D",    // Perform the subtraction
                    "@TRUE." + this.counter,   
                    "D;JEQ",    // Jump to TRUE if equal to 0
                    "@SP",      // If we're here, then false
                    "A=M-1",
                    "M=0",      // Store 0 (false) in top of stack
                    "@END." + this.counter,
                    "0;JMP",    // Jump to end
                    "(TRUE." + this.counter + ")" ,
                    "@SP",    
                    "A=M-1",
                    "M=-1",     //Store -1 (true) in top of stack
                    "(END." + this.counter + ")"
                ])
                break;
            }

            case "gt": {
                this.writeToFile([
                    "// Greater than",
                    "@SP",
                    "M=M-1",    // Decrement SP by 1
                    "A=M",
                    "D=M",      // Load top value into D
                    "@SP",
                    "A=M-1",    // Point A to second-to-top value
                    "D=M-D",    // Perform the subtraction 
                    "@TRUE." + this.counter,   
                    "D;JGT",    // Jump to TRUE if greater than 0
                    "@SP",      // If we're here, then false
                    "A=M-1",
                    "M=0",      // Store 0 (false) in top of stack
                    "@END." + this.counter,
                    "0;JMP",    // Jump to end
                    "(TRUE." + this.counter + ")" ,
                    "@SP",    
                    "A=M-1",
                    "M=-1",     //Store -1 (true) in top of stack
                    "(END." + this.counter + ")"
                ])
                break;
            }

            case "lt": {
                this.writeToFile([
                    "// Less than",
                    "@SP",
                    "M=M-1",    // Decrement SP by 1
                    "A=M",
                    "D=M",      // Load top value into D
                    "@SP",
                    "A=M-1",    // Point A to second-to-top value
                    "D=M-D",    // Perform the subtraction 
                    "@TRUE." + this.counter,   
                    "D;JLT",    // Jump to TRUE if less than 0
                    "@SP",      // If we're here, then false
                    "A=M-1",
                    "M=0",      // Store 0 (false) in top of stack
                    "@END." + this.counter,
                    "0;JMP",    // Jump to end
                    "(TRUE." + this.counter + ")" ,
                    "@SP",    
                    "A=M-1",
                    "M=-1",     //Store -1 (true) in top of stack
                    "(END." + this.counter + ")"
                ])
                break;
            }

            case "and": {
                this.writeToFile([
                    "// Bit-wise and",
                    "@SP",
                    "M=M-1",    // Decrement SP by 1
                    "A=M",
                    "D=M",      // Load top value into D
                    "@SP",
                    "A=M-1",    // Point A to second-to-top value
                    "D=D&M",    // Perform the subtraction
                    "M=D"       // Store the result at the top of the stack
                ])
                break;
            }

            case "or": {
                this.writeToFile([
                    "// Bit-wise or",
                    "@SP",
                    "M=M-1",    // Decrement SP by 1
                    "A=M",
                    "D=M",      // Load top value into D
                    "@SP",
                    "A=M-1",    // Point A to second-to-top value
                    "D=D|M",    // Perform the subtraction
                    "M=D"       // Store the result at the top of the stack
                ])
                break;
            }

            case "not": {
                this.writeToFile([
                    "// Bit-wise not",
                    "@SP",
                    "A=M-1",      // Get the last value on the stack
                    "M=!M",       // Perform the not operation and store it
                    // No need to change stack pointer
                ])
                break;
            }

            default: {
                throw "Error in CodeWriter: WriteArithmetic: command not matched";
            }
        }
    }

    writePushPop(command: string, segment: string, index: number) {

        let segment_asm: string;

        // Translate vm segment name to asm symbol
        switch (segment) {

            case "local": {
                segment_asm = "LCL";
                break;
            }
            case "argument": {
                segment_asm = "ARG";
                break;
            }
            case "this": {
                segment_asm = "THIS";
                break;
            }
            case "that": {
                segment_asm = "THAT";
                break;
            }
            case "temp": {
                segment_asm = "5"; // No asm symbol for this
                break;
            }
            case "pointer": {
                segment_asm = "3";
                break;
            }
            case "constant": {
                // Entirely virtual segment, no action required
                // But don't want to throw an error
                break;
            }
            default: {
                throw "CodeWriter Error: PushPop: segment not found";
            }
        }

        if (command == "push") {

            if (segment == "constant") {
                this.writeToFile([
                    // Store constant in D
                    "// Push constant " + index + " to stack",
                    "@" + index,
                    "D=A",
                ]);
            } 
            else if (segment == "temp" || segment == "pointer") {
                // Fetch source value and store in D
                // This is different because these are fixed ranges, we are not dereferencing a pointer as with other segments
                this.writeToFile([
                    "// Push value to stack from " + segment + "[" + index + "]",
                    "@" + segment_asm,
                    "D=A",
                    "@" + index,
                    "A=D+A",
                    "D=M"
                ])                
            }
            else {
                // Fetch source value and store in D
                this.writeToFile([
                    "// Push value to stack from " + segment + "[" + index + "]",
                    "@" + segment_asm,
                    "D=M",
                    "@" + index,
                    "A=D+A",
                    "D=M"
                ])
            }

            // Write D value to stack (loaded above) and increment SP by 1
            this.writeToFile([
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1"
            ])
        } 

        else if (command == "pop") {

            if (segment == "temp" || segment == "pointer") {
                // This is treated differently because these are fixed ranges, we don't need to dereference a pointer
                this.writeToFile([
                    "// Pop value from stack to " + segment + "[" + index + "]",
                    // Calculate and store address of destination (segment + index)
                    // This is stored in R13 (the first of general purpose registers)
                    "@" + segment_asm,
                    "D=A",
                    "@" + index,
                    "D=D+A",
                    "@R13",
                    "M=D",
                ])
            }
            else {
                this.writeToFile([
                    "// Pop value from stack to " + segment + "[" + index + "]",
                    // Calculate and store address of destination (segment + index)
                    // This is stored in R13 (the first of general purpose registers)
                    "@" + segment_asm,
                    "D=M",
                    "@" + index,
                    "D=D+A",
                    "@R13",
                    "M=D",
                ])
            }

            this.writeToFile([
                // Get value on top of stack and decrement SP
                "@SP",
                "M=M-1",
                "A=M",
                "D=M",
                // Store value in destination
                "@R13",
                "A=M",
                "M=D"
                ])

        }
        else {
            throw "Error in CodeWriter: WritePushPop: command not matched";
        }
    }

    close(){

        // Write infinite loop as standard way to terminate hack programs
        this.writeToFile([
            "// End loop",
            "(END)",
            "@END",
            "0;JMP"
        ]);
    }

    writeToFile(command: string[]){
        for (let i = 0; i < command.length; i++) {
            fs.appendFileSync(this.output, command[i] + "\n");
        }
    }

    constructor(output: string){
        this.output = output;
        fs.writeFileSync(this.output, "// Translation of " + this.output + " to ASM \n");
    }
}