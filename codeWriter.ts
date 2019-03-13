import { Writable } from 'stream';

const fs = require('fs');

export class CodeWriter {

    output: Writable;
    counter: number = 0;

    setFileName(filname: string){

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

        if (command == "push") {
            if (segment == "constant") {
                this.writeToFile([
                    "// Push constant " + index + " to stack",
                    "@" + index,    //Store constant in A
                    "D=A",          // Store constant in D
                    "@SP",          // Load SP address into A
                    "A=M",          // Load value of SP into A
                    "M=D",          // Store constant in top of stack
                    "@SP",
                    "M=M+1"         // Increment SP by 1
                ]);
            }
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
        ])

        this.output.end((err) => {
            if (err) throw err;
            console.log("Closed output file.");
        });
    }

    writeToFile(command: string[]){
        for (let i = 0; i < command.length; i++) {
            this.output.write(command[i] + "\n", (err) => {
                if (err) throw err;
            });
        }
    }

    constructor(output_filename: string){

        this.output = fs.createWriteStream(output_filename, (err) => {
            if (err) throw err;
            console.log("Successfully opened " + output_filename + " for writing.");
        });
        
    }
}