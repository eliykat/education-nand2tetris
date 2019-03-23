const fs = require('fs');

export class CodeWriter {

    output: string;
    current_class: string;
    counter: number = 0;
    current_function: string = "default";

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

    writePushPop(command: string, segment: string, index: string) {

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
            case "static": {
                // Static segment approximates fixed variables (e.g. @i)
                // So we create a unique variable name using the input filename + index number
                segment_asm = this.current_class + "." + index;
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
            else if (segment == "static") {
                // Fetch static variable and store in D
                this.writeToFile([
                    "// Push value to stack from " + segment + "[" + index + "]",
                    "@" + segment_asm,
                    "D=M"
                ]);
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
            else if (segment == "static") {
                // Static segment is treated differently due to the way it accesses fixed variables
                // This is a little inefficient because it stores the val in R13 when it doesn't need to,
                // but it maintains compatability with how the other segments work here
                this.writeToFile([
                    "// Pop value from stack to " + segment + "[" + index + "]",
                    "@" + segment_asm,
                    "D=A",
                    "@R13",
                    "M=D"
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

            // Write value to address stored in R13 (which should already be done above)
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

    writeInit() {
        // Initialise SP to 256
        this.writeToFile([
            "@256",
            "D=A",
            "@SP",
            "M=D",
        ])

        // Call sys.init function
        this.writeCall("sys.init", 0);
    }

    writeLabel(label: string) {
        this.writeToFile([
            "(" + this.current_class + "." + this.current_function + "_" + label + ")"
        ])
    }

    writeGoto(label: string) {
        //NB: this label is function scoped - so not suitable for all purposes (e.g. transferring control between functions)
        this.writeToFile([
            "@" + this.current_class + "." + this.current_function + "_" + label,
            "0;JMP"
        ])
    }

    writeIf(label: string) {
        this.writeToFile([
            "@SP",
            "M=M-1",
            "A=M",
            "D=M",
            "@" + this.current_class + "." + this.current_function + "_" + label,
            "D;JNE"  //jump if not equal to zero
        ])
    }

    writeCall(functionName: string, numArgs: number) {

        // Push return address
        this.writePushPop('push', 'constant', functionName + this.counter + ".return");

        // Push LCL pointer value
        this.writePushPop('push', 'constant', 'LCL');

        // Push ARG pointer value
        this.writePushPop('push', 'constant', 'ARG');

        // Push this pointer value
        this.writePushPop('push', 'constant', 'THIS');

        // Push that pointer value
        this.writePushPop('push', 'constant', 'THAT');

        this.writeToFile([
            // Reposition ARG pointer to SP - numArgs - 5
            "@SP",
            "D=A",
            "@" + (numArgs + 5),
            "D=D-A",
            "@ARG",
            "M=D",
            // Reposition LCL pointer to top of stack
            "@SP",
            "D=A",
            "@LCL",
            "M=D",
            // Transfer control to the called function
            "@" + functionName,
            "0;JMP",
            // Declare label for return address (this uses the counter to ensure it is unique)
            "(" + functionName + this.counter + ".return)"
        ])
    }

    writeReturn() {

        this.writeToFile([
            "// Return from function " + this.current_function,
            // FRAME is a temporary variable to keep track of where we are as we pop from the global stack around us
            "@LCL",
            "D=M",
            "@FRAME" +  this.counter,    // MAKE UNIQUE
            "M=D",
            // Put the return address in a temp var. RET = *(FRAME - 5)
            // NB: FRAME pointer already in D register
            "@5",
            "A=D-A",
            "D=M",
            "@RET"  + this.counter,     // MAKE UNIQUE
            "M=D"
        ])

        // Pop from the top of the stack (the return argument) to argument[0] (which will become the top of the caller frame shortly)
        this.writePushPop('pop', 'argument', '0');
        
        this.writeToFile([
            // Restore SP of the caller (ARG + 1)
            "@ARG",
            "D=M+1",
            "@SP",
            "M=D",
            // Return THAT of the caller
            "@FRAME" + this.counter,
            "A=M-1",
            "D=M",
            "@THAT",
            "M=D",
            // Return THIS of the caller
            "@FRAME" + this.counter,
            "A=M-1",
            "A=A-1",
            "D=M",
            "@THIS",
            "M=D",
            // Restore ARG of the caller
            "@FRAME" + this.counter,
            "A=M-1",
            "A=A-1",
            "A=A-1",
            "D=M",
            "@ARG",
            "M=D",
            // Restore LCL of the caller
            "@FRAME" + this.counter,
            "A=M-1",
            "A=A-1",
            "A=A-1",
            "A=A-1",
            "D=M",
            "@LCL",
            "M=D",
            // Transfer control back to the caller
            "@RET" + this.counter,
            "A=M",
            "0;JMP"
        ])
    }

    writeFunction(functionName: string, numLocals: number) {
        // Let the object know which function we're in - used for function-scoped labels
        this.current_function = functionName;

        // Label for function entry
        this.writeToFile([
            "// START OF " + functionName,
            "(" + functionName + ")"
        ])

        // Initialise local variables to 0
        for (let i = 0; i < numLocals; i++) {
            this.writePushPop('push', 'constant', '0');
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
        this.current_class = output.slice(output.lastIndexOf("\\") + 1, output.lastIndexOf("."));   // This is inefficient but will likely be replaced later once I figure out how to parse an entire directory
        fs.writeFileSync(this.output, "// Translation of " + this.output + " to ASM \n");
    }
}