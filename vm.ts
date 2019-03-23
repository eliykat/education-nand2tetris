import { Parser } from "./parser";
import { CodeWriter } from "./codeWriter";

const input_filename = process.argv[2];
const output_filename:string = input_filename.slice(0, input_filename.lastIndexOf(".")) + ".asm";

const parser = new Parser(input_filename);
const codeWriter = new CodeWriter(output_filename);

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