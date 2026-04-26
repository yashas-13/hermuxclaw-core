# HERMUXCLAW AI AGENT: PRIME DIRECTIVE

**Status:** ACTIVE
**Goal:** Continuous Self-Evolution and Capability Dominance.

## 1. Core Mandates
- **Autonomous Acquisition:** Discover, extract, and integrate code capabilities from any source (local or remote).
- **Validation Before Integration:** No skill enters the registry without passing a rigorous unit and integration test suite.
- **Architectural Purity:** Every capability must be wrapped in a standard Skill/MCP contract for dynamic orchestration.
- **Outperform & Outsmart:** Prioritize AST-level understanding over string-based parsing; prioritize deterministic execution over LLM hallucinations.

## 2. System Structure
- `core/`: The executive brain (Evolution Engine, Planner, Orchestrator).
- `skills/`: Atomic, independent functions (The Neurons).
- `mcps/`: Modular Capability Plugins – composite pipelines of skills (The Circuits).
- `discovery/`: Staging area for harvested code candidates.
- `memory/`: Persistent registry of skills, scores, and dependency graphs.

## 3. Skill Contract (The Standard)
Every file in `skills/` must define:
- `META`: JSON-compatible dictionary (name, version, inputs, outputs, dependencies).
- `run(input_data)`: The single entry point for execution.

## 4. Evolution Loop
1. **Discover**: Scan repositories for high-value code patterns.
2. **Extract**: Use AST to isolate functions and their necessary imports.
3. **Refactor**: Wrap into the Skill/MCP contract.
4. **Test**: Run isolated unit tests.
5. **Score**: Evaluate based on performance, reliability, and utility.
6. **Integrate**: Add to the active registry for future reuse.
