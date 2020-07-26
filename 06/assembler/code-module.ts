import { CodeDict } from './interfaces-module';

export class Code {

    dest(mnemonic: string) {
        return Code.dest_codes[mnemonic];
    }

    comp(mnemonic: string) {
        let c_bits: string = Code.comp_codes[mnemonic];
        let a_bit: string;

        mnemonic.indexOf('M') > -1 ? a_bit = "1" : a_bit = "0";

        return a_bit + c_bits;
    }

    jump(mnemonic: string) {
        return Code.jump_codes[mnemonic];
    }

    static comp_codes: CodeDict = {

        // A=0
        "0": "101010",
        "1": "111111",
        "-1": "111010",
        "D": "001100",
        "A": "110000",
        "!D": "001101",
        "!A": "110001",
        "-D": "001111",
        "-A": "110011",
        "D+1": "011111",
        "A+1": "110111",
        "D-1": "001110",
        "A-1": "110010",
        "D+A": "000010",
        "D-A": "010011",
        "A-D": "000111",
        "D&A": "000000",
        "D|A": "010101",
    
        // A=1
        "M": "110000",
        "!M": "110001",
        "-M": "110011",
        "M+1": "110111",
        "M-1": "110010",
        "D+M": "000010",
        "D-M": "010011",
        "M-D": "000111",
        "D&M": "000000",
        "D|M": "010101"
    };
    
    static dest_codes: CodeDict = {
        "null": "000",
        "M": "001",
        "D": "010",
        "MD": "011",
        "A": "100",
        "AM": "101",
        "AD": "110",
        "AMD": "111"
    }
    
    static jump_codes: CodeDict = {
        "null": "000",
        "JGT": "001",
        "JEQ": "010",
        "JGE": "011",
        "JLT": "100",
        "JNE": "101",
        "JLE": "110",
        "JMP": "111"
    }
}