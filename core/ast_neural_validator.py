import os
import sys
import ast

sys.path.append(os.path.expanduser("~/hermuxclaw"))
from core.ast_mutator import SafeMutator
from core.log_manager import get_logger

class ASTNeuralValidator:
    """
    Structural DNA Editor for HermuXclaw-CORE.
    Ensures LLM suggestions obey strict AST-node validity checks.
    """
    def __init__(self):
        self.logger = get_logger("ASTValidator")

    def validate_and_refactor(self, original_code, neural_suggestion):
        """
        Validates the suggestion and performs structural alignment.
        """
        try:
            # 1. Syntax Check
            suggested_tree = ast.parse(neural_suggestion)
            
            # 2. Structural Analysis: Does it preserve core function signatures?
            # We compare the names of functions in the original vs the new
            original_tree = ast.parse(original_code)
            
            orig_funcs = {n.name for n in ast.walk(original_tree) if isinstance(n, ast.FunctionDef)}
            new_funcs = {n.name for n in ast.walk(suggested_tree) if isinstance(n, ast.FunctionDef)}
            
            if not orig_funcs.issubset(new_funcs):
                missing = orig_funcs - new_funcs
                self.logger.error(f"Neural suggestion deleted core functions: {missing}", "StructuralLoss")
                return None # Reject if core logic is missing

            # 3. Final Pass: Use SafeMutator to cleanup any artifacts
            mutator = SafeMutator(mutation_rate=0) # Pure cleanup mode
            final_tree = mutator.visit(suggested_tree)
            ast.fix_missing_locations(final_tree)
            
            return ast.unparse(final_tree)
            
        except Exception as e:
            self.logger.error(f"AST Validation failed: {e}", "SyntaxError")
            return None

if __name__ == "__main__":
    validator = ASTNeuralValidator()
    print("[*] AST Neural Validator Initialized.")
