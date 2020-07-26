fs = require('fs');

let string = "";

for (var i = 0; i < 16; i++) {

    // Convert i to 15 bit binary9
    var binary = Number(i).toString(2); // only handles unsigned numbers
    binary = binary.padStart(15,'0');

    string += '"R' + i + '": "' + binary + '", \n';
}

fs.writeFile('r_codes.txt', string, (err) => {
    if (err) throw err;
    console.log('Wrote line' + i);
});
