#!venv/bin/python
from compiler import compile, pprint_ast
from compiler import (
    ProgramNode,
    StatementNode,
    ReducedNode,
    FullNode,
    OriginNode,
    TermNode,
    Operand,
    Next,
)
from anytree import NodeMixin

from typing import Callable


filename = "program.subleq"

ast = compile(
    filename,
    #    logging_level=20,
    log_file=None,
)


# def visit_nodes(node, is_node_type, perform):
#     if is_node_type(node):
#         perform(node)
#     if isinstance(node, dict):
#         for key, value in node.items():
#             visit_nodes(value, is_node_type, perform)
#     elif isinstance(node, list):
#         for value in node:
#             visit_nodes(value, is_node_type, perform)


# def find_reduced(node):
#     print(f"{node.keys()=}  {type(node)=}")
#     if not isinstance(node, dict):
#         return
#     if node.name == "reduced":
#         pprint_ast(node)


# visit_nodes(ast, find_reduced, lambda _: None)


def visit_nodes(root: NodeMixin, name: str, func: Callable):
    """
    Visit all nodes with a name attribute that matches the given name parameter,
    and perform the given function on each visited node.
    """
    for node in root.descendants:
        if isinstance(node, NodeMixin) and node.name == name:
            func(node)


def replace_reduced_nodes(root: NodeMixin):
    for node in root.descendants:
        if isinstance(node, ReducedNode):
            print(f"looking at {node=}")
            if node.order == 3:
                new_node = FullNode(node.children)
                new_node.parent = node.parent
                node.parent.children = [new_node]
                continue
            if node.order == 2:
                term0 = TermNode(node.children[0].label, node.children[0].operand)
                term1 = TermNode(node.children[1].label, node.children[1].operand)
                new_node = FullNode([term0, term1, Next()])
                new_node.parent = node.parent
                node.parent.children = [new_node]
                continue
            if node.order == 1:
                term0 = TermNode(node.children[0].label, node.children[0].operand)
                term1 = TermNode(node.children[0].label, node.children[0].operand)
                new_node = FullNode([term0, term1, Next()])
                new_node.parent = node.parent
                node.parent.children = [new_node]
                continue


pprint_ast(ast)
# visit_nodes(ast, "reduced", lambda node: pprint_ast(node))
replace_reduced_nodes(ast)

pprint_ast(ast)
