from . import tokenizer
from . import compiler
from .compiler import compile
from .compiler import (
    ProgramNode,
    StatementNode,
    ReducedNode,
    FullNode,
    OriginNode,
    TermNode,
    Operand,
    Next,
)
from ply.lex import LexToken as Token


def pprint_ast(ast):
    from anytree import RenderTree

    for pre, _, node in RenderTree(ast):
        if isinstance(node, TermNode):
            treestr = f"{pre}{node.name} label={node.label} operand={node.operand}"
        else:
            treestr = "%s%s" % (pre, node.name)
        # print(treestr.ljust(8), node.length, node.width)
        print(treestr)
