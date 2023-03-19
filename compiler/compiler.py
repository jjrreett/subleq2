from __future__ import annotations
import logging
from ply.lex import LexToken
from compiler.tokenizer import generate_tokens
from typing import Optional
from anytree import NodeMixin, RenderTree


def log_calls(func):
    def wrapper(stack, **kwargs):
        logging.info(f"Call {func.__name__}() with, {stack[0] = }")
        result = func(stack, **kwargs)
        logging.debug(f"Return {func.__name__}() returned {result}")
        return result

    return wrapper


def slow():
    # import time
    # time.sleep(0.01)
    return


class ProgramNode(NodeMixin):
    def __init__(self, children: list[StatementNode]) -> None:
        """
        Program Node is intended to be the root of the ast
        args:
            childrent [list]: list of StatementNodes
        """
        self.name = "program"
        self.parent = None
        self.children = children


@log_calls
def program(stack: list[LexToken]):
    """program : statement*"""
    slow()

    statements = []
    while len(stack) > 0:
        statements.append(statement(stack))

    return ProgramNode(children=statements)
    return {"program": statements}


class StatementNode(NodeMixin):
    def __init__(self, child: MacroNode | FullNode | ReducedNode) -> None:
        """
        creates a statement node
        args:
            child: MacroNode | FullNode | ReducedNode - a single node
        """
        self.name = "statement"
        self.parent = None
        self.children = [child]


@log_calls
def statement(stack: list[LexToken]):
    """statement : reduced | full | origin"""
    slow()
    if x := macro(stack):
        return StatementNode(x)

    if x := full(stack):
        return StatementNode(x)

    if x := reduced(stack):
        return StatementNode(x)

    if x := origin(stack):
        return StatementNode(x)


class MacroNode(NodeMixin):
    def __init__(
        self, id: LexToken, args: list[LexToken], children: list[StatementNode]
    ) -> None:
        self.id = id
        self.name = "macro"
        self.parent = None
        self.args = args
        self.children = children


@log_calls
def macro(stack: list[LexToken]):
    """macro : IDENTIFIER IDENTIFIER* '{' statement* '}'"""
    slow()
    if stack[0].type != "MACRO":
        return None
    stack.pop(0)

    if stack[0].type != "IDENTIFIER":
        raise SyntaxError(f"expecting IDENTIFIER after MACRO, got {stack[0]}")
    identifier = stack.pop(0)

    args = []
    while True:
        if stack[0].type == "{":
            stack.pop(0)
            break
        if stack[0].type != "IDENTIFIER":
            raise SyntaxError(
                f"expecting IDENTIFIER after as macro arguments, got {stack[0]}"
            )
        args.append(stack.pop(0))

    statements = []
    while stack[0].type != "}":
        statements.append(statement(stack))
    stack.pop(0)

    return MacroNode(identifier, args, statements)


class ReducedNode(NodeMixin):
    def __init__(self, children: list[LexToken]) -> None:
        self.name = "reduced"
        self.parent = None
        self.children = children
        self.order = len(children)


@log_calls
def reduced(stack: list[LexToken]):
    """reduced : term{1,3} ';'"""
    slow()

    if not (tm := term(stack)):
        return None

    tms = [tm]
    for _ in range(2):
        if tm := term(stack):
            tms.append(tm)

    if stack[0].type == ";":
        stack.pop(0)
        return ReducedNode(tms)

    raise SyntaxError(f"was expecting ;, got {stack[0]}")


class FullNode(NodeMixin):
    def __init__(self, children) -> None:
        self.name = "full"
        self.parent = None
        self.children = children


@log_calls
def full(stack: list[LexToken]):
    """full : '[' term* ']'"""
    slow()

    if stack[0].type != "[":
        return None
    stack.pop(0)

    tms = []
    while True:
        if len(stack) <= 0:
            raise SyntaxError("full must be terminated with a ';'")
        if tm := term(stack):
            tms.append(tm)
        if stack[0].type == "]":
            stack.pop(0)
            # TODO add check for end of stack raise syntax error
            return FullNode(tms)


class OriginNode(NodeMixin):  # leaf
    def __init__(self, address) -> None:
        self.name = "origin"
        self.parent = None
        self.address = address
        # self.children = children


@log_calls
def origin(stack: list[LexToken]):
    """origin : ORIGIN NUMBER"""
    slow()
    if stack[0].type != "ORIGIN":
        return None
    stack.pop(0)
    if stack[0].type != "NUMBER":
        raise SyntaxError("expecting type number after .org")
    token = stack.pop(0)
    # QUESTION, if origin can only be numbers, why do we need to keep the type

    return OriginNode(token.value)


class TermNode(NodeMixin):  # leaf
    def __init__(self, label, operand) -> None:
        self.name = "term"
        self.parent = None
        self.label = label
        self.operand = operand
        # self.children = children


@log_calls
def term(stack: list[LexToken]):
    """term : label* operand"""
    slow()
    # if there is a label, label() will shift the stack
    # else it will return None
    lb = label(stack)
    op = operand(stack)
    if lb is None and op is None:
        return None
    return TermNode(lb, op)


@log_calls
def label(stack: list[LexToken]):  # attribute
    """label: IDENTIFIER ':'"""
    slow()

    if stack[0].type != "IDENTIFIER":
        return None

    if stack[1].type == ":":
        token = stack.pop(0)
        stack.pop(0)  # pop the colon
        # QUESTION, if labels can only be identifiers, why do we need to keep the type
        return token.value

    return None


class Operand:  # leaf # TODO should probably a NodeMixin
    def __init__(self, type, value) -> None:
        self.name = "operand"
        self.type = type
        self.value = value

    def __repr__(self):
        return f"<{self.type} {self.value}>"


class Next(NodeMixin):  # leaf
    def __init__(self) -> None:
        self.name = "next"

    def __repr__(self):
        return f"<next>"


@log_calls
def operand(stack: list[LexToken]):
    """operand: NUMBER | IDENTIFIER | '?'"""
    slow()
    if stack[0].type in ("NUMBER", "IDENTIFIER"):
        token = stack.pop(0)
        return Operand(token.type, token.value)
    if stack[0].type == "?":
        token = stack.pop(0)
        return Next()

    return None


def generate_ast(tokens: list[LexToken]) -> dict:
    return program(tokens)


def compile(
    filename: str, logging_level: int = 30, log_file: Optional[str] = "compiler.log"
) -> dict:
    """
    Parse the assembly file at the given path and return the AST as a tree structure.

    Args:
        filename (str): The path to the assembly file.

    Keyword Args:
        debug_level (int): The logging level to use. Defaults to 30.
            10-DEBUG,
            20-INFO,
            30-WARNING,
            40-ERROR,
            50-CRITICAL,
        log_file (Optional[str]): The output log file. Defaults to 'compiler.log'.
            If set to None, output goes to the console.

    Returns:
        dict: The AST as a tree structure.
    """

    logging.basicConfig(filename=log_file, level=logging_level)
    tokens = generate_tokens(filename)
    return program(tokens)


# def main():
#     # from pprint import pprint as print

#     # import yaml

#     # def custom_representations(dumper, data):
#     #     return dumper.represent_scalar("!LexToken", data.__repr__())

#     # # Register the custom representations with PyYAML
#     # yaml.add_representer(LexToken, custom_representations)

#     # class IndentDumper(yaml.Dumper):
#     #     def increase_indent(self, flow=False, indentless=False):
#     #         return super(IndentDumper, self).increase_indent(flow, False)

#     # def print_tree_as_yaml(tree):
#     #     yaml_output = yaml.dump(tree, sort_keys=False, Dumper=IndentDumper)
#     #     print(yaml_output)

#     ast = generate_ast("program.subleq")
#     print(ast)
#     # print_tree_as_yaml(ast)


# def pprint_ast(ast):
#     for pre, _, node in RenderTree(ast):
#         treestr = "%s%s" % (pre, node.name)
#         # print(treestr.ljust(8), node.length, node.width)
#         print(treestr)


# if __name__ == "__main__":
#     main()


# TODO(bear) try out ?
#            try out ?+1
#            compile it
#                find all operands of type IDENTIFIER
#                find all label nodes with corosponding label
