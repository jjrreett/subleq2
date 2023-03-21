#!venv/bin/python
grammer = r"""
program =
    (statement nl?)*

statement =
    macro /
    macro_call /
    reduced /
    full /
    origin

macro =
    "macro" _ identifier "(" (ws? identifier)* ws? ")" ws? "{" (ws? statement)* ws? "}"

macro_call =
    identifier "(" (ws? identifier)* ws? ")"

reduced =
    (ws? term){1,3} ws? ";"

full =
    "[" (ws? term)* ws? "]"

origin =
    ".org" _ number 

term = 
    label? ws? operand?

label =
    identifier ws? ":"

operand =
    identifier /
    address

address =
    specific_address / 
    local_address

specific_address = 
    "&" _? number

local_address =
    "?" _? offset?

offset = ("+"/"-") _? number

identifier = ~r"[_A-Za-z][_A-Za-z0-9]*"
number = ~r"(0x[0-9abcdeABCDEF]+|0b[01]+|[0-9]+)"
ws = ~"[ \t\n]"
nl = ~"\n"
_ = " "
"""
"""    "(" address ")" /"""

from parsimonious.grammar import Grammar

grammer = Grammar(grammer)

file_name = "program2.subleq"
with open(file_name) as file:
    data = file.read()

print(grammer.parse(data))
