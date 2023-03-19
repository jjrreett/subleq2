import ply.lex as lex

literals = [
    ":",
    ";",
    "[",
    "]",
    "?",
    "(",
    ")",
    "{",
    "}",
    ",",
]

# List of token names.   This is always required
tokens = (
    "MACRO",
    "ORIGIN",
    "COMMENT",
    "NUMBER",
    "IDENTIFIER",
)

# t_MACRO = r"macro"
t_ORIGIN = r"\.org"

# # Regular expression rules for simple tokens
# t_SEMICOLON = r";"
# t_LSQBRACKET = r"\["
# t_RSQBRACKET = r"\]"
# t_COLON = r":"
t_ignore_COMMENT = r"\#.*"


def t_MACRO(t):
    r"macro"
    return t


def t_NUMBER(t):
    r"(0x[0-9abcdeABCDEF]+|0b[01]+|[0-9]+)"
    t.value = eval(t.value)
    return t


def t_IDENTIFIER(t):
    r"[_A-Za-z][_A-Za-z0-9]*"
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = " \t"


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def generate_tokens(file_name):
    with open(file_name) as file:
        data = file.read()

    lexer = lex.lex()
    lexer.input(data)
    return [tok for tok in lexer]


def main():
    from pprint import pprint as print

    tokens = generate_tokens("program.subleq")
    print(tokens)


if __name__ == "__main__":
    main()
