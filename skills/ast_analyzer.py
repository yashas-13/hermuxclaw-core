import ast
import os
import json

META = {
    "name": "ast_analyzer",
    "version": "1.0",
    "description": "Deep AST-based code analysis and capability extraction.",
    "inputs": ["file_path"],
    "outputs": ["structure_map", "extracted_capabilities"]
}

class HermuxclawASTParser(ast.NodeVisitor):
    def __init__(self, source_code):
        self.tree = ast.parse(source_code)
        self.stats = {
            "functions": [],
            "classes": [],
            "imports": [],
            "async_functions": 0
        }

    def visit_Import(self, node):
        for alias in node.names:
            self.stats["imports"].append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        self.stats["imports"].append(node.module)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        func_info = {
            "name": node.name,
            "args": [arg.arg for arg in node.args.args],
            "line": node.lineno,
            "is_async": False,
            "docstring": ast.get_docstring(node)
        }
        self.stats["functions"].append(func_info)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        func_info = {
            "name": node.name,
            "args": [arg.arg for arg in node.args.args],
            "line": node.lineno,
            "is_async": True,
            "docstring": ast.get_docstring(node)
        }
        self.stats["functions"].append(func_info)
        self.stats["async_functions"] += 1
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        class_info = {
            "name": node.name,
            "methods": [n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))],
            "line": node.lineno
        }
        self.stats["classes"].append(class_info)
        self.generic_visit(node)

    def analyze(self):
        self.visit(self.tree)
        return self.stats

def run(input_data):
    """
    Primary entry point for the AST Analyzer skill.
    input_data: dict containing 'file_path' or 'source_code'
    """
    file_path = input_data.get("file_path")
    source_code = input_data.get("source_code")

    if file_path and os.path.exists(file_path):
        with open(file_path, "r") as f:
            source_code = f.read()
    
    if not source_code:
        return {"status": "error", "message": "No source code provided."}

    try:
        parser = HermuxclawASTParser(source_code)
        analysis = parser.analyze()
        return {"status": "success", "data": analysis}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # Self-test: Analyze this very file
    result = run({"file_path": __file__})
    print(json.dumps(result, indent=2))
