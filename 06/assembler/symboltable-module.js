"use strict";
exports.__esModule = true;
var SymbolTable = /** @class */ (function () {
    function SymbolTable() {
        this.symbols = {};
    }
    SymbolTable.prototype.addEntry = function (symbol, address) {
        this.symbols[symbol] = address;
    };
    SymbolTable.prototype.contains = function (symbol) {
        if (symbol in this.symbols || symbol in SymbolTable.builtin_symbols) {
            return true;
        }
        else {
            return false;
        }
    };
    SymbolTable.prototype.getAddress = function (symbol) {
        // Fetches from the builtin symbols first, which ensures they can't be overridden
        if (symbol in SymbolTable.builtin_symbols) {
            return SymbolTable.builtin_symbols[symbol];
        }
        else {
            return this.symbols[symbol];
        }
    };
    SymbolTable.builtin_symbols = {
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "SCREEN": 16384,
        "KBD": 24576,
        "R0": 0,
        "R1": 1,
        "R2": 2,
        "R3": 3,
        "R4": 4,
        "R5": 5,
        "R6": 6,
        "R7": 7,
        "R8": 8,
        "R9": 9,
        "R10": 10,
        "R11": 11,
        "R12": 12,
        "R13": 13,
        "R14": 14,
        "R15": 15
    };
    return SymbolTable;
}());
exports.SymbolTable = SymbolTable;
