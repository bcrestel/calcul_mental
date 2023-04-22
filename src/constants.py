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