"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var fs = require('fs');
var CodeWriter = /** @class */ (function () {
    function CodeWriter(output_filename) {
        this.counter = 0;
        this.output = fs.createWriteStream(output_filename, function (err) {
            if (err)
                throw err;
            console.log("Successfully opened " + output_filename + " for writing.");
        });
    }
    CodeWriter.prototype.setFileName = function (filname) {
    };
    CodeWriter.prototype.writeArithmetic = function (command) {
        // Increment the unique counter by 1,
        // regardless of which type of command it is
        this.counter += 1;
        switch (command) {
            case "add": {
                this.writeToFile([
                    "// Add",
                    "@SP",
                    "M=M-1",
                    "A=M",
                    "D=M",
                    "@SP",
                    "A=M-1",
                    "D=D+M",
                    "M=D" // Store the result at the top of the stack
                ]);
                break;
            }
            case "sub": {
                this.writeToFile([
                    "// Subtract",
                    "@SP",
                    "M=M-1",
                    "A=M",
                    "D=M",
                    "@SP",
                    "A=M-1",
                    "D=M-D",
                    "M=D" // Store the result at the top of the stack
                ]);
                break;
            }
            case "neg": {
                this.writeToFile([
                    "// Negation",
                    "@SP",
                    "A=M-1",
                    "M=-M",
                ]);
                break;
            }
            case "eq": {
                this.writeToFile([
                    "// Eq",
                    "@SP",
                    "M=M-1",
                    "A=M",
                    "D=M",
                    "@SP",
                    "A=M-1",
                    "D=M-D",
                    "@TRUE." + this.counter,
                    "D;JEQ",
                    "@SP",
                    "A=M-1",
                    "M=0",
                    "@END." + this.counter,
                    "0;JMP",
                    "(TRUE." + this.counter + ")",
                    "@SP",
                    "A=M-1",
                    "M=-1",
                    "(END." + this.counter + ")"
                ]);
                break;
            }
            case "gt": {
                this.writeToFile([
                    "// Greater than",
                    "@SP",
                    "M=M-1",
                    "A=M",
                    "D=M",
                    "@SP",
                    "A=M-1",
                    "D=M-D",
                    "@TRUE." + this.counter,
                    "D;JGT",
                    "@SP",
                    "A=M-1",
                    "M=0",
                    "@END." + this.counter,
                    "0;JMP",
                    "(TRUE." + this.counter + ")",
                    "@SP",
                    "A=M-1",
                    "M=-1",
                    "(END." + this.counter + ")"
                ]);
                break;
            }
            case "lt": {
                this.writeToFile([
                    "// Less than",
                    "@SP",
                    "M=M-1",
                    "A=M",
                    "D=M",
                    "@SP",
                    "A=M-1",
                    "D=M-D",
                    "@TRUE." + this.counter,
                    "D;JLT",
                    "@SP",
                    "A=M-1",
                    "M=0",
                    "@END." + this.counter,
                    "0;JMP",
                    "(TRUE." + this.counter + ")",
                    "@SP",
                    "A=M-1",
                    "M=-1",
                    "(END." + this.counter + ")"
                ]);
                break;
            }
            case "and": {
                this.writeToFile([
                    "// Bit-wise and",
                    "@SP",
                    "M=M-1",
                    "A=M",
                    "D=M",
                    "@SP",
                    "A=M-1",
                    "D=D&M",
                    "M=D" // Store the result at the top of the stack
                ]);
                break;
            }
            case "or": {
                this.writeToFile([
                    "// Bit-wise or",
                    "@SP",
                    "M=M-1",
                    "A=M",
                    "D=M",
                    "@SP",
                    "A=M-1",
                    "D=D|M",
                    "M=D" // Store the result at the top of the stack
                ]);
                break;
            }
            case "not": {
                this.writeToFile([
                    "// Bit-wise not",
                    "@SP",
                    "A=M-1",
                    "M=!M",
                ]);
                break;
            }
            default: {
                throw "Error in CodeWriter: WriteArithmetic: command not matched";
            }
        }
    };
    CodeWriter.prototype.writePushPop = function (command, segment, index) {
        if (command == "push") {
            if (segment == "constant") {
                this.writeToFile([
                    "// Push constant " + index + " to stack",
                    "@" + index,
                    "D=A",
                    "@SP",
                    "A=M",
                    "M=D",
                    "@SP",
                    "M=M+1" // Increment SP by 1
                ]);
            }
        }
        else {
            throw "Error in CodeWriter: WritePushPop: command not matched";
        }
    };
    CodeWriter.prototype.close = function () {
        // Write infinite loop as standard way to terminate hack programs
        this.writeToFile([
            "// End loop",
            "(END)",
            "@END",
            "0;JMP"
        ]);
        this.output.end(function (err) {
            if (err)
                throw err;
            console.log("Closed output file.");
        });
    };
    CodeWriter.prototype.writeToFile = function (command) {
        for (var i = 0; i < command.length; i++) {
            this.output.write(command[i] + "\n", function (err) {
                if (err)
                    throw err;
            });
        }
    };
    return CodeWriter;
}());
exports.CodeWriter = CodeWriter;
