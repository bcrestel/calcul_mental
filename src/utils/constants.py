from enum import Enum

file_path = "src/logs"


class Operation(Enum):
    multiplication = "*"
    addition = "+"
    soustraction = "-"
    division = "/"


map_sym_text_op = {
    "*": Operation.multiplication,
    "+": Operation.addition,
    "-": Operation.soustraction,
    "/": Operation.division,
}


map_sym_2_text = {
    "*": "la multiplication",
    "+": "l'addition",
    "-": "la soustraction",
    "/": "la division"
}

factor_change_in_weights = 2.0
