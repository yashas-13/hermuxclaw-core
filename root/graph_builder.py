import ast
import os
import sys

sys.path.append(os.path.expanduser("~/hermuxclaw"))
from knowledge.graph_store import graph_store

class GraphBuilder(ast.NodeVisitor):
    """
    AST Graph Reconstructor.
    Builds the structural graph from source code.
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.current_function = "module_scope"
        self.store = graph_store

    def build(self):
        if not os.path.exists(self.file_path): return
        with open(self.file_path, "r") as f:
            try:
                tree = ast.parse(f.read())
                self.visit(tree)
            except:
                pass

    def visit_FunctionDef(self, node):
        prev_func = self.current_function
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = prev_func

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)

    def visit_Call(self, node):
        callee = None
        if isinstance(node.func, ast.Name):
            callee = node.func.id
        elif isinstance(node.func, ast.Attribute):
            callee = node.func.attr
            
        if callee:
            self.store.add_call(self.current_function, callee)
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            self.store.add_dependency(self.file_path, alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            self.store.add_dependency(self.file_path, node.module)
        self.generic_visit(node)
