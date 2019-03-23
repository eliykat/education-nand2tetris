"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var parser_1 = require("./parser");
var codeWriter_1 = require("./codeWriter");
var input_filename = process.argv[2];
var output_filename = input_filename.slice(0, input_filename.lastIndexOf(".")) + ".asm";
var parser = new parser_1.Parser(input_filename);
var codeWriter = new codeWriter_1.CodeWriter(output_filename);
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
codeWriter.close();
console.log("All done!");
