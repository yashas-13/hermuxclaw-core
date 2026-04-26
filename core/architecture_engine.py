import ast
import os
import json
import sys
from collections import deque

# Ensure core is accessible
sys.path.append(os.path.expanduser("~/hermuxclaw"))
from core.runtime_tracer import RuntimeTracer
from core.anomaly_detector import AnomalyDetector

class GlobalSymbolTable:
    def __init__(self):
        self.functions = {} # name -> file_path
        self.classes = {}   # name -> file_path
        self.imports = {}   # file_path -> list of imports

    def register_module(self, file_path, ast_data):
        for fn in ast_data.get("functions", []):
            self.functions[fn["name"]] = file_path
        for cls in ast_data.get("classes", []):
            self.classes[cls["name"]] = file_path
        self.imports[file_path] = ast_data.get("imports", [])

class ArchitectureAnalyzer(ast.NodeVisitor):
    def __init__(self, file_path, symbol_table):
        self.file_path = file_path
        self.symbol_table = symbol_table
        self.calls = []
        self.dependencies = []

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.calls.append(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            self.calls.append(node.func.attr)
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            self.dependencies.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            self.dependencies.append(node.module)
        self.generic_visit(node)

class RootIntelligenceV2:
    """
    The Advanced Hybrid Architecture Engine for Hermuxclaw.
    Performs cross-file symbol resolution, runtime-behavior merging, and anomaly detection.
    """
    def __init__(self, workspace_root):
        self.root = workspace_root
        self.symbol_table = GlobalSymbolTable()
        self.call_graph = {} # caller_file -> [target_files]
        self.dep_graph = {}  # file -> [imported_modules]
        self.arch_map = {}
        self.runtime_trace = []
        self.tracer = RuntimeTracer(workspace_root)
        self.detector = None

    def ingest_workspace(self, run_tracing=False, target_workload=None):
        print(f"[*] Root Intelligence: Mapping Workspace Architecture...")
        
        # 1. RUNTIME TRACING (Behavioral Truth)
        if run_tracing and target_workload:
            self.tracer.start()
            try:
                target_workload()
            except Exception as e:
                print(f"[!] Workload Error during tracing: {e}")
            finally:
                self.tracer.stop()
                self.runtime_trace = self.tracer.trace_data
                self.tracer.save_trace()

        # 2. STATIC ANALYSIS (Structural Framework)
        from skills import ast_analyzer
        files_to_process = []
        for root, _, files in os.walk(self.root):
            if any(x in root for x in [".git", "node_modules", "__pycache__", "memory"]): continue
            for f in files:
                if f.endswith(".py"):
                    files_to_process.append(os.path.join(root, f))

        # Pass 1: Build Global Symbol Table
        for fpath in files_to_process:
            res = ast_analyzer.run({"file_path": fpath})
            if res["status"] == "success":
                self.symbol_table.register_module(fpath, res["data"])

        # Pass 2: Build Call and Dependency Graphs
        for fpath in files_to_process:
            with open(fpath, "r") as f:
                try:
                    tree = ast.parse(f.read())
                    analyzer = ArchitectureAnalyzer(fpath, self.symbol_table)
                    analyzer.visit(tree)
                    
                    resolved_calls = []
                    for call in analyzer.calls:
                        target = self.symbol_table.functions.get(call) or self.symbol_table.classes.get(call)
                        if target and target != fpath:
                            resolved_calls.append(target)
                    
                    self.call_graph[fpath] = list(set(resolved_calls))
                    self.dep_graph[fpath] = list(set(analyzer.dependencies))
                except:
                    continue

        self._merge_runtime_data()
        self._build_architecture_map()

    def _merge_runtime_data(self):
        """Merge captured runtime calls into the static call graph for truth verification."""
        if not self.runtime_trace: return
        
        print(f"[*] Merging {len(self.runtime_trace)} runtime events into architecture map...")
        for entry in self.runtime_trace:
            fpath = os.path.join(self.root, entry["file"])
            if fpath in self.call_graph:
                target_file = self.symbol_table.functions.get(entry["callee"])
                if target_file and target_file not in self.call_graph[fpath]:
                    self.call_graph[fpath].append(target_file)

    def _build_architecture_map(self):
        for fpath in self.dep_graph:
            rel_path = os.path.relpath(fpath, self.root)
            calls = [os.path.relpath(c, self.root) for c in self.call_graph.get(fpath, [])]
            
            num_calls = len(calls)
            num_deps = len(self.dep_graph[fpath])
            
            layer = "utility"
            if num_calls > 3 and num_deps < 2: layer = "entry"
            elif num_deps > 3: layer = "core"
            
            self.arch_map[rel_path] = {
                "layer": layer,
                "calls": calls,
                "dependencies": self.dep_graph[fpath],
                "score": num_calls + num_deps
            }
        
        # 3. ANOMALY DETECTION
        self.detector = AnomalyDetector(self.arch_map)
        self.detector.detect()

    def generate_full_report(self):
        report = []
        report.append("\n" + "="*60)
        report.append("HERMUXCLAW HYBRID INTELLIGENCE REPORT")
        report.append("="*60)
        
        for file, data in self.arch_map.items():
            report.append(f"[{data['layer'].upper()}] {file} (Complexity: {data['score']})")
            
        report.append("\n" + self.detector.generate_report())
        report.append("\n" + "="*60)
        return "\n".join(report)

    def generate_dot_graph(self):
        dot = ["digraph HERMUXCLAW_ARCH {", "  rankdir=LR;", "  node [shape=box, style=filled, fontname=Arial];"]
        colors = {"entry": "lightblue", "core": "lightsalmon", "utility": "lightgray"}
        for file, data in self.arch_map.items():
            color = colors.get(data["layer"], "white")
            dot.append(f'  "{file}" [fillcolor={color}, label="{file}\\n({data["layer"]})"];')
            for target in data["calls"]:
                dot.append(f'  "{file}" -> "{target}" [color=blue];')
        dot.append("}")
        return "\n".join(dot)

if __name__ == "__main__":
    engine = RootIntelligenceV2(os.path.expanduser("~/hermuxclaw"))
    
    def workload():
        # A simple workload to trace: Initialize the core and register a skill
        from core.evolution_engine import HermuxclawCore
        core = HermuxclawCore()
        
    engine.ingest_workspace(run_tracing=True, target_workload=workload)
    print(engine.generate_full_report())
    
    # Save DOT graph
    dot_graph = engine.generate_dot_graph()
    with open(os.path.expanduser("~/hermuxclaw/memory/architecture.dot"), "w") as f:
        f.write(dot_graph)
    print(f"\n[✓] Hybrid Architecture Map saved to ~/hermuxclaw/memory/architecture.dot")
