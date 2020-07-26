"use strict";
exports.__esModule = true;
var fs = require('fs');
var Parser = /** @class */ (function () {
    function Parser(filename) {
        this.asm = [];
        // The API specifies that "initially there should be no current command".
        // Therefore these values are initialised to dummy values
        this.readLine = -1;
        this.command = "";
        this.jump_index = -1;
        this.dest_index = -1;
        var dirty_asm_input = fs.readFileSync(filename);
        var dirty_asm = dirty_asm_input.toString().split("\n");
        var trimmed;
        for (var i = 0; i < dirty_asm.length; i++) {
            if (!this.ignoreLine(dirty_asm[i])) {
                trimmed = dirty_asm[i].trim();
                this.asm.push(trimmed);
            }
        }
    }
    Parser.prototype.hasMoreCommands = function () {
        if (this.readLine + 1 == this.asm.length) {
            return false;
        }
        else {
            return true;
        }
    };
    Parser.prototype.advance = function () {
        // Advance the cursor by 1
        this.readLine += 1;
        // Set the current command (really just a shortform reference)
        this.command = this.asm[this.readLine];
        // Determine the jump and dest indexes
        this.jump_index = this.command.indexOf(";");
        this.dest_index = this.command.indexOf("=");
    };
    Parser.prototype.commandType = function () {
        if (this.command[0] == '@') {
            return 'A_COMMAND';
        }
        else if (this.command[0] == "(") {
            return 'L_COMMAND';
        }
        else {
            return 'C_COMMAND';
        }
    };
    Parser.prototype.symbol = function () {
        // TODO
    };
    Parser.prototype.dest = function () {
        if (this.dest_index > -1) {
            return this.command.slice(0, this.dest_index);
        }
        else {
            return "null";
        }
    };
    Parser.prototype.comp = function () {
        var start;
        var end;
        this.dest_index > -1 ? start = this.dest_index + 1 : start = 0;
        this.jump_index > -1 ? end = this.jump_index : end = this.command.length;
        return this.command.slice(start, end);
    };
    Parser.prototype.jump = function () {
        if (this.jump_index > -1) {
            return this.command.slice(this.jump_index + 1, this.command.length);
        }
        else {
            return "null";
        }
    };
    Parser.prototype.ignoreLine = function (line) {
        // Returns true if a string is a comment or blank/empty line
        if (line.search(/^\s*\/\//) > -1 || line.search(/^\s*$/) > -1 || line.search(/^\n$/) > -1) {
            return true;
        }
        return false;
    };
    Parser.prototype.reset = function () {
        this.readLine = -1;
    };
    return Parser;
}());
exports.Parser = Parser;
