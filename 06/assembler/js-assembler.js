var fs = require('fs');

var asm = process.argv[2];
var output_filename = asm.slice(0, asm.lastIndexOf(".")) + ".hack"

var output = "";

var comp_dict = {

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

var dest_dict = {
    "null": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

var jump_dict = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

// Built in symbols
var symbols_dict = {
    "SP": "000000000000000",
    "LCL": "000000000000001",
    "ARG": "000000000000010",
    "THIS": "000000000000011",
    "THAT": "000000000000100",
    "SCREEN": "100000000000000",
    "KBD": "011000000000000"
}

// Populate symbols dict with R* addresses that I am too lazy to type
for (var i = 0; i < 16; i++) {

    // Convert i to 15 bit binary
    var binary = Number(i).toString(2); // only handles unsigned numbers
    binary = binary.padStart(15,'0');

    symbols_dict["R" + i] = binary;
}


console.log('Opening ' + asm);

fs.readFile(asm, (err, data) => {
    var array = data.toString().split("\n");

    for (var i = 0; i < array.length; i++) {

        // Check for comment
        if ( array[i].search(/^\s*\/\//) > -1 ) {
            continue;
        }

        // Check for empty line
        if (array[i].search(/^\s*$/) > -1 || array[i].search(/^\n$/) > -1) {
            continue;
        }

        // Check for 

        // A INSTRUCTION
        if (array[i][0] == '@') {

            // Convert v bits into decimal
            var aValueDecimal = array[i].slice(1);
            var aValueBinary = Number(aValueDecimal).toString(2); // only handles unsigned numbers
            
            // Pad with leding zeroes (noting that first bit is a zero)
            aValueBinary = aValueBinary.padStart(16,'0');
            
            output += aValueBinary + "\n";

        } 
        
        // C INSTRUCTION
        else {
            var dest_index = array[i].indexOf("=");
            var jump_index = array[i].indexOf(";");

            if (dest_index > -1 && jump_index > -1) {
                // The C instruction has both jump and dest bits (plus comp)

                var dest_asm = array[i].slice(0,dest_index);
                var comp_asm = array[i].slice(dest_index + 1, jump_index);
                var jump_asm = array[i].slice(jump_index + 1, array[i].length -1);

            } else if (dest_index > -1) {
                // The C instruction has dest bits only (plus comp)
                
                var dest_asm = array[i].slice(0,dest_index);
                var comp_asm = array[i].slice(dest_index + 1, array[i].length -1);
                var jump_asm = "null";

            } else if (jump_index > -1) { 
                // The C instruction has jump bits only (plus comp)

                var dest_asm = "null";
                var comp_asm = array[i].slice(0,jump_index);
                var jump_asm = array[i].slice(jump_index + 1, array[i].length -1);

            }
            else {
                // The C instruction does not have jump or dest bits
                // which is theoretically possible but doesn't do anything and is likely a mistake

                console.log("error");
            }

            var comp_bits = comp_dict[comp_asm];
            var dest_bits = dest_dict[dest_asm];
            var jump_bits = jump_dict[jump_asm];

            // Set A bit based on whether the comp instruction refers to the M register or not
            if (comp_asm.indexOf('M') > -1) {
                var a_bit = "1";
            } else {
                var a_bit = "0";
            }

            // Compile the final C instruction
            output += "111" + a_bit + comp_bits + dest_bits + jump_bits + "\n";           

        }

    }

    saveFile();

})

function saveFile () {
    fs.writeFile(output_filename, output, (err) => {
        if (err){
            throw err;
        } else {
            console.log ('Successfully translated file and saved as ' + output_filename + ".");
        }
    });    
}