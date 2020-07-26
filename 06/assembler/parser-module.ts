var fs = require('fs');

export class Parser {

    asm: string[] = [];

    // The API specifies that "initially there should be no current command".
    // Therefore these values are initialised to dummy values
    readLine: number = -1;
    command: string = "";
    jump_index: number = -1;
    dest_index: number = -1;

    hasMoreCommands(): boolean {
        if (this.readLine + 1 == this.asm.length) {
            return false;
        } else {
            return true;
        }
    }

    advance() {
        // Advance the cursor by 1
        this.readLine += 1;

        // Set the current command (really just a shortform reference)
        this.command = this.asm[this.readLine];

        // Determine the jump and dest indexes
        this.jump_index = this.command.indexOf(";");
        this.dest_index = this.command.indexOf("=");
    }

    commandType(): string {
        if (this.command[0] == '@') {
            return 'A_COMMAND';
        } else if (this.command[0] == "(") {
            return 'L_COMMAND';
        } else {
            return 'C_COMMAND';
        }
    }

    symbol() {
        // TODO
    }

    dest(): string {
        if (this.dest_index > -1) {
            return this.command.slice(0,this.dest_index);
        } else {
            return "null";
        }
    }

    comp(): string {
        let start: number;
        let end: number;

        this.dest_index > -1 ? start = this.dest_index + 1 : start = 0;
        this.jump_index > -1 ? end = this.jump_index : end = this.command.length;

        return this.command.slice(start, end);
    }

    jump(): string {
        if (this.jump_index > -1) {
            return this.command.slice(this.jump_index + 1, this.command.length);
        } else {
            return "null";
        }
    }

    ignoreLine(line: string) {
        // Returns true if a string is a comment or blank/empty line

        if ( line.search(/^\s*\/\//) > -1 || line.search(/^\s*$/) > -1 || line.search(/^\n$/) > -1 ) {
            return true;
        }

        return false;
    }

    reset() {
        this.readLine = -1;
    }

    constructor(filename: string) {
        
        var dirty_asm_input = fs.readFileSync(filename);
        var dirty_asm = dirty_asm_input.toString().split("\n");
        let trimmed: string;

        for (var i = 0; i < dirty_asm.length; i++) {
            if (!this.ignoreLine(dirty_asm[i])) {

                trimmed = dirty_asm[i].trim();

                this.asm.push(trimmed);
            }
        }
    }
}