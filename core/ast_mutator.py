import ast
import random
import sys

class SafeMutator(ast.NodeTransformer):
    """
    AST-Safe Mutation Engine.
    Safely mutates Python code without breaking its syntactic structure.
    Operations include: Constant jittering, Operator swapping, Statement shuffling.
    """
    def __init__(self, mutation_rate=0.1):
        self.mutation_rate = mutation_rate
        self.mutations_applied = []

    def visit_Constant(self, node):
        if random.random() < self.mutation_rate:
            if isinstance(node.value, int) and not isinstance(node.value, bool):
                # Jitter integers by +/- 1
                new_val = node.value + random.choice([-1, 1])
                self.mutations_applied.append(f"Changed int {node.value} to {new_val}")
                return ast.Constant(value=new_val)
            elif isinstance(node.value, float):
                # Jitter floats by +/- 5%
                new_val = node.value * random.uniform(0.95, 1.05)
                self.mutations_applied.append(f"Changed float {node.value} to {new_val}")
                return ast.Constant(value=new_val)
            elif isinstance(node.value, str):
                pass # Don't mutate strings blindly to avoid breaking keys/URLs
        return self.generic_visit(node)

    def visit_BinOp(self, node):
        # Swap operators safely
        if random.random() < self.mutation_rate:
            ops = {
                ast.Add: ast.Sub(),
                ast.Sub: ast.Add(),
                ast.Mult: ast.Div(),
                ast.Div: ast.Mult()
            }
            for op_type, new_op in ops.items():
                if isinstance(node.op, op_type):
                    self.mutations_applied.append(f"Swapped binary operator {op_type.__name__} to {type(new_op).__name__}")
                    return ast.BinOp(left=self.visit(node.left), op=new_op, right=self.visit(node.right))
        return self.generic_visit(node)

    def visit_Compare(self, node):
        if random.random() < self.mutation_rate and len(node.ops) == 1:
            op = node.ops[0]
            swaps = {
                ast.Lt: ast.LtE(),
                ast.LtE: ast.Lt(),
                ast.Gt: ast.GtE(),
                ast.GtE: ast.Gt(),
                ast.Eq: ast.NotEq(),
                ast.NotEq: ast.Eq()
            }
            for op_type, new_op in swaps.items():
                if isinstance(op, op_type):
                    self.mutations_applied.append(f"Swapped comparison {op_type.__name__} to {type(new_op).__name__}")
                    return ast.Compare(
                        left=self.visit(node.left),
                        ops=[new_op],
                        comparators=[self.visit(c) for c in node.comparators]
                    )
        return self.generic_visit(node)


def ast_mutate(code_string, mutation_rate=0.1):
    """
    Parses code into AST, applies safe mutations, and unparses back to a string.
    Returns (mutated_code_string, list_of_mutations_applied).
    """
    try:
        tree = ast.parse(code_string)
        mutator = SafeMutator(mutation_rate=mutation_rate)
        mutated_tree = mutator.visit(tree)
        ast.fix_missing_locations(mutated_tree)
        
        # In Python 3.9+, ast.unparse converts AST back to source code
        mutated_code = ast.unparse(mutated_tree)
        return mutated_code, mutator.mutations_applied
    except Exception as e:
        # If parsing or unparsing fails, return the original code safely
        print(f"[!] AST Mutation Failed: {e}")
        return code_string, []

if __name__ == "__main__":
    sample_code = """
def calculate(x, y):
    threshold = 100
    if x > threshold:
        return x + y * 2
    return x - y
"""
    print("Original Code:")
    print(sample_code)
    
    mutated, changes = ast_mutate(sample_code, mutation_rate=1.0) # 100% mutation rate for testing
    
    print("\nMutated Code:")
    print(mutated)
    
    print("\nChanges Applied:")
    for change in changes:
        print(f" - {change}")
