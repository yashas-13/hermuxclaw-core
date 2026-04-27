# skills/ast_extractor_skill.py
import ast, inspect, textwrap
from skills.base_skill import BaseSkill

class ASTExtractorSkill(BaseSkill):
    """
    Core AST Engine.
    Extracts specific logic blocks from raw Python files and formats them into Skill templates.
    """
    META = {
        "name": "ast_extractor_skill",
        "version": "1.0.0",
        "inputs": ["source_code", "target_function"],
        "outputs": ["extracted_code", "imports", "skill_template"],
        "dependencies": []
    }

    def run(self, input_data):
        source = input_data["source_code"]
        target = input_data.get("target_function")
        
        # Parse the raw source
        tree = ast.parse(source)
        imports, funcs = [], []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                imports.append(ast.unparse(node))
            elif isinstance(node, ast.FunctionDef):
                if not target or node.name == target:
                    funcs.append(ast.unparse(node))
        
        extracted = funcs[0] if funcs else ""
        template = self._wrap_skill(extracted, imports)
        
        return {
            "extracted_code": extracted,
            "imports": imports, 
            "skill_template": template
        }

    def _wrap_skill(self, func_code, imports):
        # Programmatically wrap extracted code into the HermuXclaw Class format
        return textwrap.dedent(f"""
            {chr(10).join(imports)}
            from skills.base_skill import BaseSkill
            
            class ExtractedSkill(BaseSkill):
                META = {{"name": "extracted", "version": "1.0.0",
                        "inputs": [], "outputs": [], "dependencies": []}}
                
                def run(self, input_data):
                    {func_code.replace(chr(10), chr(10)+'    ')}
        """)
