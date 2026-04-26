import os
import sys
import ast

sys.path.append(os.path.expanduser("~/hermuxclaw"))
from core.semantic_indexer import SemanticIndexer

class RootDiscovery:
    """
    AST-Powered Deep Code Discovery.
    Traverses directories and extracts structurally rich fragments (functions, classes).
    """
    def __init__(self):
        self.scanned_hashes = set()

    def discover_ast_fragments(self, directory, max_depth=3):
        fragments = []
        for root, dirs, files in os.walk(directory):
            if any(ignore in root for ignore in [".git", "hermuxclaw/memory", "__pycache__"]):
                continue
                
            for f in files:
                if f.endswith(".py"):
                    filepath = os.path.join(root, f)
                    try:
                        with open(filepath, "r", encoding="utf-8") as file:
                            code = file.read()
                            
                            h = hash(code)
                            if h in self.scanned_hashes:
                                continue
                            self.scanned_hashes.add(h)
                            
                            # Standard ast parsing to find semantic blocks
                            tree = ast.parse(code)
                            for node in ast.walk(tree):
                                if isinstance(node, ast.FunctionDef):
                                    doc = ast.get_docstring(node) or ""
                                    args = [a.arg for a in node.args.args]
                                    
                                    # CLASSIFICATION LOGIC
                                    classification = self._classify_logic(node, code)
                                    
                                    desc = f"[{classification}] Function '{node.name}' taking arguments {args}. "
                                    if doc:
                                        desc += f"Description: {doc}"
                                    
                                    fragments.append({
                                        "type": "function",
                                        "name": node.name,
                                        "description": desc,
                                        "classification": classification,
                                        "file": filepath,
                                        "line": node.lineno
                                    })
                                elif isinstance(node, ast.ClassDef):
                                    doc = ast.get_docstring(node) or ""
                                    methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                                    
                                    # Simple class classification based on methods
                                    classification = "CORE_LOGIC"
                                    if any(x in node.name.lower() for x in ["db", "store", "memory", "file"]):
                                        classification = "DATA_IO"
                                    
                                    desc = f"[{classification}] Class '{node.name}' with methods {methods}. "
                                    if doc:
                                        desc += f"Description: {doc}"
                                        
                                    fragments.append({
                                        "type": "class",
                                        "name": node.name,
                                        "description": desc,
                                        "classification": classification,
                                        "file": filepath,
                                        "line": node.lineno
                                    })
                    except Exception as e:
                        # Skip files that fail to parse
                        pass
        return fragments

    def _classify_logic(self, node, full_code):
        """Heuristic-based segmentation of logic blocks."""
        name = node.name.lower()
        
        # 1. NETWORK segment
        if any(x in name for x in ["request", "socket", "http", "api", "url", "swarm", "fetch"]):
            return "NETWORK"
            
        # 2. DATA / IO segment
        if any(x in name for x in ["db", "save", "load", "write", "read", "file", "json", "sql"]):
            return "DATA_IO"
            
        # 3. UTILITY segment
        if any(x in name for x in ["helper", "util", "parse", "format", "check", "verify"]):
            return "UTILITY"
            
        # Default
        return "CORE_LOGIC"

class RootFilter:
    """
    Semantic Filtering of AST Fragments.
    """
    def __init__(self, indexer):
        self.indexer = indexer

    def index_fragments(self, fragments):
        added = 0
        for frag in fragments:
            doc_id = f"{frag['file']}::{frag['name']}"
            if doc_id not in self.indexer.index:
                # We embed the description of the AST node
                success = self.indexer.add_document(
                    doc_id=doc_id, 
                    text=frag["description"], 
                    metadata=frag
                )
                if success:
                    added += 1
        return added

    def find_relevant(self, query, top_k=3):
        return self.indexer.search(query, top_k=top_k)

class RootSystem:
    """
    Orchestrates AST Discovery and Semantic Indexing.
    The true brain of Hermuxclaw's capabilities.
    """
    def __init__(self, core_system):
        self.system = core_system # HermuxclawCore
        self.discovery = RootDiscovery()
        self.indexer = SemanticIndexer()
        self.filter = RootFilter(self.indexer)

    def harvest_semantically(self, target_directories):
        print(f"\n[🧠 ROOT SYSTEM] Initiating Deep AST Semantic Harvest...")
        
        all_fragments = []
        for d in target_directories:
            if os.path.exists(d):
                print(f"  [🔍] AST Discovery: Scanning {d}...")
                all_fragments.extend(self.discovery.discover_ast_fragments(d))
                
        print(f"  [📚] Indexing {len(all_fragments)} AST fragments into Semantic Memory...")
        new_indexed = self.filter.index_fragments(all_fragments)
        print(f"  [+] Added {new_indexed} new embeddings to the Semantic Index.")
        
        return new_indexed

if __name__ == "__main__":
    from core.evolution_engine import HermuxclawCore
    core = HermuxclawCore()
    rs = RootSystem(core)
    rs.harvest_semantically([os.path.expanduser("~/hermuxclaw/core")])
