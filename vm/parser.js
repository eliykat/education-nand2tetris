"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var fs = require('fs');
var Parser = /** @class */ (function () {
    function Parser(filename) {
        this.line = -1;
        this.input = [];
        var input_file = fs.readFileSync(filename);
        var dirty_input = input_file.toString().split("\n");
        var trimmed;
        var comment;
        for (var i = 0; i < dirty_input.length; i++) {
            // Remove whitespace at start and end of line
            trimmed = dirty_input[i].trim();
            // Skip if line is empty
            if (trimmed.length < 1)
                continue;
            // Check for double forwardslash, indicating that line is a comment
            comment = trimmed.indexOf("//");
            if (comment > -1) {
                // Skip whole line if comment is at the start
                if (comment == 0)
                    continue;
                // Assume the comment is at the end of a command - drop the comment only
                trimmed = trimmed.slice(0, comment);
            }
            // Remove whitespace at start and end of line (again)
            trimmed = trimmed.trim();
            // Push onto cleaned up input
            this.input.push(trimmed);
        }
        console.log("Successfully loaded " + filename + " for compiling.");
    }
    Parser.prototype.hasMoreCommands = function () {
        if (this.line + 1 == this.input.length) {
            return false;
        }
        else {
            return true;
        }
    };
    Parser.prototype.advance = function () {
        this.line += 1;
        this.command = this.input[this.line];
        this.commandArray = this.command.split(" ");
        if (this.commandArray.length < 1)
            throw "Parser Error: Advance: empty command";
    };
    Parser.prototype.commandType = function () {
        switch (this.commandArray[0]) {
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
    };
    Parser.prototype.arg1 = function () {
        if (this.commandArray.length < 2)
            throw "Parser: Arg1: tried to access arg1 when it does not exist.";
        return this.commandArray[1];
    };
    Parser.prototype.arg2 = function () {
        if (this.commandArray.length < 3)
            throw "Parser: Arg2: tried to access arg2 when it does not exist.";
        return this.commandArray[2];
    };
    return Parser;
}());
exports.Parser = Parser;
