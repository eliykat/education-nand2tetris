const fs = require('fs');

export class Parser {

    command: string;
    commandArray: string[];
    line: number = -1;
    input: string[] = [];

    hasMoreCommands(): boolean {
        if (this.line + 1 == this.input.length) {
            return false;
        } else {
            return true;
        }
    }

    advance() {
        this.line += 1;
        this.command = this.input[this.line];
        this.commandArray = this.command.split(" ");

        if (this.commandArray.length < 1) throw "Parser Error: Advance: empty command";
    }

    commandType(): string {

        switch(this.commandArray[0]) {

            // Arithmetic commands
            case "add": return "C_ARITHMETIC";
            case "sub": return "C_ARITHMETIC";
            case "neg": return "C_ARITHMETIC";
            case "eq": return "C_ARITHMETIC";
            case "gt": return "C_ARITHMETIC";
            case "lt": return "C_ARITHMETIC";
            case "and": return "C_ARITHMETIC";
            case "or": return "C_ARITHMETIC";
            case "not": return "C_ARITHMETIC";

            // Memory access commands
            case "push": return "C_PUSH";
            case "pop": return "C_POP";

            // Program flow commands
            case "goto": return "C_GOTO";
            case "if-goto": return "C_IF";
            case "label": return "C_LABEL";

            // Function commands
            case "function": return "C_FUNCTION";
            case "return": return "C_RETURN";
            case "call": return "C_CALL";

            default: throw "Parser Error: CommandType: command not matched";
        }
    }

    arg1(): string {
        if (this.commandArray.length < 2) throw "Parser: Arg1: tried to access arg1 when it does not exist.";
        return this.commandArray[1];
    }

    arg2(): string {
        if (this.commandArray.length < 3) throw "Parser: Arg2: tried to access arg2 when it does not exist.";
        return this.commandArray[2];
    }

    ignoreLine(line: string) {
        // Returns true if a string is a comment or blank/empty line

        if ( line.search(/^\s*\/\//) > -1 || line.search(/^\s*$/) > -1 || line.search(/^\n$/) > -1 ) {
            return true;
        }

        return false;
    }

    constructor(filename: string) {

        var input_file = fs.readFileSync(filename);
        var dirty_input = input_file.toString().split("\n");
        let trimmed: string;

        for (var i = 0; i < dirty_input.length; i++) {
            if (!this.ignoreLine(dirty_input[i])) {

                trimmed = dirty_input[i].trim();

                this.input.push(trimmed);
            }
        }

        console.log("Successfully loaded " + filename + " for compiling.")

    }
}