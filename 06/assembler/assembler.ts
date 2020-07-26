import { Parser } from './parser-module';
import { Code } from './code-module';
import { SymbolTable } from './symboltable-module';

const fs = require('fs');

let input_filename: string = process.argv[2];
let output_filename:string = input_filename.slice(0, input_filename.lastIndexOf(".")) + ".hack";
let output: string = "";

const parser: Parser = new Parser(input_filename);
const code: Code = new Code;
const symbolTable: SymbolTable = new SymbolTable

// First loop - log symbols to the symbolTable only

let instructionCount = -1;

do {
    parser.advance()

    if (parser.commandType() == 'L_COMMAND') {
        let symbol = parser.command.slice(1, parser.command.length -1 );

        if (!symbolTable.contains(symbol)) {
            symbolTable.addEntry(symbol, instructionCount + 1 );
        }
    } else {
        instructionCount += 1;
    }

} while (parser.hasMoreCommands());

console.log("Custom symbolTable:")
console.log(symbolTable.symbols);

parser.reset();

// This is the address at which variables are stored, starting at 16 as per specifications
let nextVariableAddress: number = 16;

// Second loop - fill in all symbols and variables
do {
    parser.advance();
    if (parser.commandType() == 'C_COMMAND') {

        let comp_mnemonic = parser.comp();
        let dest_mnemonic = parser.dest();
        let jump_mnemonic = parser.jump();

        output += "111" + code.comp(comp_mnemonic) + 
            code.dest(dest_mnemonic) + code.jump(jump_mnemonic) + "\n";

    } else if (parser.commandType() == 'A_COMMAND') {

        let value = parser.command.slice(1);

        // Check if it contains any symbols
        if (value.search(/[A-z]/) > -1) {

            if (symbolTable.contains(value)) {
                // This is a label or stored variable that we can retrieve
                value = symbolTable.getAddress(value).toString(2);
            } else {
                // This is a new variable we need to allocate an address to
                symbolTable.addEntry(value, nextVariableAddress);
                value = nextVariableAddress.toString(2);
                nextVariableAddress += 1;
            }            
        } else {
            value = Number(value).toString(2); // only handles unsigned numbers
        }

        // Extract decimal value of the A command and convert to binary
        
        // Pad with leading zeroes (noting that first bit is a zero)
        value = value.padStart(16,'0');
        
        output += value + "\n";
    }

} while (parser.hasMoreCommands());

// Write the output file.
fs.writeFile(output_filename, output, (err: any) => {
    if (err) throw err;
    console.log("Successfully wrote output to " + output_filename + ".");
})