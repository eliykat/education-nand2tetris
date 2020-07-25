const fs = require('fs');
const path = require('path');

import { Parser } from "./parser";
import { CodeWriter } from "./codeWriter";

let input = process.argv[2];
let output_filename: string

const parserArray: Parser[] = [];
const filenameArray: string[] = [];


// Test if directory or single .vm file
if (fs.lstatSync(input).isDirectory()) {

    // Make sure the input directory string ends in a backslash (this is an assumption for all following code)
    if (input[input.length-1] != "\\") input = input + "\\";

    // Get directory contents, and create a new Parser object for each .vm file
    let readDir = fs.readdirSync(input);

    for (let i = 0; i < readDir.length; i++) {
        if (path.extname(readDir[i]) == ".vm") {
            parserArray.push(new Parser(input + readDir[i]));
            filenameArray.push(readDir[i].slice(0, readDir[i].lastIndexOf('.')));
        }
    }

    // Set output filename - this gets the directory name and appends .asm
    output_filename = input + input.match(/(?<=\\)\w*(?=\\$)/)[0] + ".asm";

} else {

    // Make sure it is a vm file, else throw an error
    if (path.extname(input) != ".vm") {
        throw "Error: You must provide a directory or a .vm file for translation."
    }

    parserArray.push(new Parser(input));
    filenameArray.push(input);

    // Set output filename
    output_filename = input.slice(0, input.lastIndexOf(".")) + ".asm";
}

const codeWriter = new CodeWriter(output_filename);

codeWriter.writeInit();

for (let i = 0; i < parserArray.length; i++) {

    codeWriter.setFileName(filenameArray[i]);

    let parser: Parser = parserArray[i];

    do {
        parser.advance();
        
        switch (parser.commandType()) {
            case "C_ARITHMETIC": {
                codeWriter.writeArithmetic(parser.command);
                break;
            }
            case "C_PUSH": {
                codeWriter.writePushPop("push", parser.arg1(), parser.arg2());
                break;
            }
            case "C_POP": {
                codeWriter.writePushPop("pop", parser.arg1(), parser.arg2());
                break;
            }
            case "C_GOTO": {
                codeWriter.writeGoto(parser.arg1());
                break;
            }
            case "C_IF": {
                codeWriter.writeIf(parser.arg1());
                break;
            }
            case "C_LABEL": {
                codeWriter.writeLabel(parser.arg1());
                break;
            }
            case "C_FUNCTION": {
                codeWriter.writeFunction(parser.arg1(), Number(parser.arg2()));
                break;
            }
            case "C_RETURN": {
                codeWriter.writeReturn();
                break;
            }
            case "C_CALL": {
                codeWriter.writeCall(parser.arg1(), Number(parser.arg2()));
                break;
            }
            default: {
                throw "VM Error: CommandType not matched";
            }
        }
        
    } while (parser.hasMoreCommands());    
}

codeWriter.close();

console.log("All done!");