"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var fs = require('fs');
var path = require('path');
var parser_1 = require("./parser");
var codeWriter_1 = require("./codeWriter");
var input = process.argv[2];
var output_filename;
var parserArray = [];
var filenameArray = [];
// Test if directory or single .vm file
if (fs.lstatSync(input).isDirectory()) {
    // Make sure the directory ends in a backslash (this is an assumption for all following code)
    if (input[input.length - 1] != "\\")
        input = input + "\\";
    // Get directory contents, and create a new Parser object for each .vm file
    var readDir = fs.readdirSync(input);
    for (var i = 0; i < readDir.length; i++) {
        if (path.extname(readDir[i]) == ".vm") {
            parserArray.push(new parser_1.Parser(input + readDir[i]));
            filenameArray.push(readDir[i].slice(0, readDir[i].lastIndexOf('.')));
        }
    }
    // Set output filename - this gets the directory name and appends .asm
    output_filename = input + input.match(/(?<=\\)\w*(?=\\$)/)[0] + ".asm";
}
else {
    // Make sure it is a vm file, else throw an error
    if (path.extname(input) != ".vm") {
        throw "Error: You must provide a directory or a .vm file for translation.";
    }
    parserArray.push(new parser_1.Parser(input));
    filenameArray.push(input);
    // Set output filename
    output_filename = input.slice(0, input.lastIndexOf(".")) + ".asm";
}
var codeWriter = new codeWriter_1.CodeWriter(output_filename);
codeWriter.writeInit();
for (var i = 0; i < parserArray.length; i++) {
    codeWriter.setFileName(filenameArray[i]);
    var parser = parserArray[i];
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
