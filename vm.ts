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
    }
    
} while (parser.hasMoreCommands());

codeWriter.close();

console.log("All done!");