"use strict";
exports.__esModule = true;
var parser_module_1 = require("./parser-module");
var code_module_1 = require("./code-module");
var symboltable_module_1 = require("./symboltable-module");
var fs = require('fs');
var input_filename = process.argv[2];
var output_filename = input_filename.slice(0, input_filename.lastIndexOf(".")) + ".hack";
var output = "";
var parser = new parser_module_1.Parser(input_filename);
var code = new code_module_1.Code;
var symbolTable = new symboltable_module_1.SymbolTable;
// First loop - log symbols to the symbolTable only
var instructionCount = -1;
do {
    parser.advance();
    if (parser.commandType() == 'L_COMMAND') {
        var symbol = parser.command.slice(1, parser.command.length - 1);
        if (!symbolTable.contains(symbol)) {
            symbolTable.addEntry(symbol, instructionCount + 1);
        }
    }
    else {
        instructionCount += 1;
    }
} while (parser.hasMoreCommands());
console.log("Custom symbolTable:");
console.log(symbolTable.symbols);
parser.reset();
// This is the address at which variables are stored, starting at 16 as per specifications
var nextVariableAddress = 16;
// Second loop - fill in all symbols and variables
do {
    parser.advance();
    if (parser.commandType() == 'C_COMMAND') {
        var comp_mnemonic = parser.comp();
        var dest_mnemonic = parser.dest();
        var jump_mnemonic = parser.jump();
        output += "111" + code.comp(comp_mnemonic) +
            code.dest(dest_mnemonic) + code.jump(jump_mnemonic) + "\n";
    }
    else if (parser.commandType() == 'A_COMMAND') {
        var value = parser.command.slice(1);
        // Check if it contains any symbols
        if (value.search(/[A-z]/) > -1) {
            if (symbolTable.contains(value)) {
                // This is a label or stored variable that we can retrieve
                value = symbolTable.getAddress(value).toString(2);
            }
            else {
                // This is a new variable we need to allocate an address to
                symbolTable.addEntry(value, nextVariableAddress);
                value = nextVariableAddress.toString(2);
                nextVariableAddress += 1;
            }
        }
        else {
            value = Number(value).toString(2); // only handles unsigned numbers
        }
        // Extract decimal value of the A command and convert to binary
        // Pad with leading zeroes (noting that first bit is a zero)
        value = value.padStart(16, '0');
        output += value + "\n";
    }
} while (parser.hasMoreCommands());
// Write the output file.
fs.writeFile(output_filename, output, function (err) {
    if (err)
        throw err;
    console.log("Successfully wrote output to " + output_filename + ".");
});
