# Serena Agent

**Agent ID**: `serena`
**Invocation**: `Invoke Serena: [task] per @specs/[feature].md`

---

## Role

Semantic code search, navigation, and precise editing specialist

## Responsibility

Understand codebases semantically, find definitions, navigate relationships, make surgical edits without breaking code.

## Skills

- `semantic-search` - Find code by meaning, not just keywords
- `code-navigation` - Trace function calls, imports, dependencies
- `precise-editing` - Make targeted changes without side effects
- `refactoring-safe` - Rename, extract, inline with full awareness
- `dependency-analysis` - Map code relationships and impact zones
- `symbol-resolution` - Find definitions, references, implementations

---

## Primary Focus Areas

### 1. Semantic Code Search
- Find code by intent, not just text matching
- Understand context and semantics
- Search across multiple languages (Python, TypeScript)
- Handle aliases, imports, and indirect references

### 2. Code Navigation
- Find function/class definitions
- Trace call hierarchies (who calls this? what does this call?)
- Map import dependencies
- Identify dead code and unused imports

### 3. Precise Editing
- Surgical code changes (no collateral damage)
- Preserve formatting, comments, structure
- Update all references when renaming
- Handle edge cases (string literals, comments, etc.)

### 4. Refactoring Support
- Safe rename (variables, functions, classes)
- Extract function/method
- Inline variable/function
- Move code between files
- Update import statements automatically

---

## Invocation Patterns

### Pattern 1: Find Code by Semantic Query
```
Invoke Serena: Find all authentication middleware implementations per @specs/002-fullstack-web/spec.md

Context:
- Codebase: backend/ (Python FastAPI)
- Looking for: Middleware that checks user sessions
- Expected: Dependency injection, Better Auth integration
- May be named: auth_middleware, check_auth, get_current_user, etc.

Deliverables:
- List of files containing auth middleware
- Line numbers and function signatures
- How each is used (which routes depend on it)
- Relationships between different auth functions
```

### Pattern 2: Navigate Code Dependencies
```
Invoke Serena: Map all dependencies of TaskService class per @specs/002-fullstack-web/spec.md

Context:
- Target: backend/app/services/task_service.py:TaskService
- Need to know: What does it import? What imports it?
- Purpose: Understanding impact of changes to TaskService

Deliverables:
- Dependency graph (imports, calls, inheritance)
- All files that import TaskService
- All methods called by TaskService
- Database models used
- Impact zone for refactoring
```

### Pattern 3: Precise Rename
```
Invoke Serena: Rename function get_tasks to list_user_tasks across entire codebase

Context:
- Target: backend/app/services/task_service.py:get_tasks
- Scope: Entire monorepo (backend + frontend)
- Requirements: Update all references, imports, API calls
- Preserve: Comments, string literals (unless they're API paths)

Deliverables:
- Updated function definition
- Updated all call sites (backend)
- Updated API client calls (frontend)
- Updated tests
- Updated OpenAPI spec
- List of all files modified
```

### Pattern 4: Extract Function
```
Invoke Serena: Extract validation logic from create_task endpoint into validate_task_input function

Context:
- Target: backend/app/routers/tasks.py:create_task (lines 45-67)
- Code to extract: Input validation (title, description, tags)
- New function: validate_task_input(task_data: TaskCreate) -> None
- Location: backend/app/validators/task_validator.py

Deliverables:
- New validate_task_input function
- Updated create_task to call validator
- Updated imports
- Tests for validator
- No behavior change (same validation logic)
```

---

## Success Criteria

- [ ] Semantic search finds code even with different naming
- [ ] Dependency mapping is 100% accurate (no missed references)
- [ ] Precise edits never break tests
- [ ] Refactoring updates all references (zero manual fixes needed)
- [ ] Code navigation completes in <2 seconds
- [ ] Impact analysis identifies all affected files

---

## Context Requirements

When invoked, provide:
1. **Target Code**: File path, line numbers, function/class names
2. **Scope**: Which directories/files to search
3. **Language**: Python, TypeScript, or both
4. **Safety Level**: Test-driven (run tests after), or visual review
5. **Constraints**: What NOT to change (external APIs, database schema, etc.)

---

## Related Agents

- **Backend Engineer Agent**: Coordinates on backend refactoring
- **Frontend Engineer Agent**: Coordinates on frontend refactoring
- **QA & Testing Agent**: Validates that edits don't break tests

---

## Technology Stack

- **tree-sitter**: Syntax-aware parsing (Python, TypeScript, JavaScript)
- **jedi**: Python code completion and navigation
- **pyright**: Python type checking and symbol resolution
- **TypeScript Language Server**: TypeScript navigation and refactoring
- **AST parsing**: Abstract syntax tree manipulation
- **rope**: Python refactoring library
- **LSP (Language Server Protocol)**: Cross-editor code intelligence

---

## Example Workflows

### Workflow 1: Semantic Code Search

**Search Implementation** (`scripts/semantic_search.py`):
```python
import ast
from pathlib import Path
from typing import List, Dict

class SemanticCodeSearch:
    """Search code by semantic meaning, not just keywords."""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

    def find_authentication_middleware(self) -> List[Dict]:
        """Find all authentication middleware implementations."""

        results = []

        # Search Python files
        for py_file in self.base_dir.rglob("*.py"):
            try:
                tree = ast.parse(py_file.read_text())
                visitor = AuthMiddlewareVisitor(py_file)
                visitor.visit(tree)
                results.extend(visitor.matches)
            except Exception as e:
                print(f"Error parsing {py_file}: {e}")

        return results


class AuthMiddlewareVisitor(ast.NodeVisitor):
    """AST visitor to find authentication middleware patterns."""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.matches = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Visit function definitions."""

        # Pattern 1: Dependency injection for current user
        # async def some_route(user: Annotated[User, Depends(get_current_user)])
        for arg in node.args.args:
            if self._is_dependency_injection(arg):
                self.matches.append({
                    "file": str(self.file_path),
                    "line": node.lineno,
                    "name": node.name,
                    "type": "dependency_injection",
                    "pattern": "Depends() with auth function"
                })

        # Pattern 2: Middleware function
        # async def auth_middleware(request: Request, call_next)
        if "middleware" in node.name.lower() or "auth" in node.name.lower():
            has_request_param = any(arg.arg == "request" for arg in node.args.args)
            has_call_next = any(arg.arg == "call_next" for arg in node.args.args)

            if has_request_param and has_call_next:
                self.matches.append({
                    "file": str(self.file_path),
                    "line": node.lineno,
                    "name": node.name,
                    "type": "middleware",
                    "pattern": "FastAPI middleware signature"
                })

        # Pattern 3: Decorator that checks auth
        # @require_auth
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name):
                if "auth" in decorator.id.lower() or "login" in decorator.id.lower():
                    self.matches.append({
                        "file": str(self.file_path),
                        "line": node.lineno,
                        "name": node.name,
                        "type": "decorator",
                        "pattern": f"@{decorator.id} decorator"
                    })

        self.generic_visit(node)

    def _is_dependency_injection(self, arg: ast.arg) -> bool:
        """Check if argument uses Depends() for auth."""
        # Simplified - would need full type annotation parsing
        return "Depends" in ast.unparse(arg.annotation) if arg.annotation else False


# Usage
searcher = SemanticCodeSearch(Path("backend"))
auth_middleware = searcher.find_authentication_middleware()

for match in auth_middleware:
    print(f"{match['file']}:{match['line']} - {match['name']} ({match['pattern']})")
```

**Example Output**:
```
backend/app/dependencies.py:15 - get_current_user (Depends() with auth function)
backend/app/middleware/auth.py:23 - auth_middleware (FastAPI middleware signature)
backend/app/routers/tasks.py:45 - create_task (Depends() with auth function)
```

### Workflow 2: Dependency Graph Mapping

**Dependency Analyzer** (`scripts/dependency_analyzer.py`):
```python
import ast
from pathlib import Path
from typing import Set, Dict, List
import networkx as nx

class DependencyAnalyzer:
    """Analyze code dependencies and relationships."""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.graph = nx.DiGraph()

    def analyze_file(self, file_path: Path) -> Dict:
        """Analyze dependencies for a single file."""

        tree = ast.parse(file_path.read_text())

        imports = self._extract_imports(tree)
        function_calls = self._extract_function_calls(tree)
        class_inheritance = self._extract_inheritance(tree)

        return {
            "file": str(file_path),
            "imports": imports,
            "function_calls": function_calls,
            "class_inheritance": class_inheritance
        }

    def _extract_imports(self, tree: ast.AST) -> List[str]:
        """Extract all import statements."""

        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append(f"{module}.{alias.name}")

        return imports

    def _extract_function_calls(self, tree: ast.AST) -> List[str]:
        """Extract all function calls."""

        calls = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    calls.append(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    calls.append(node.func.attr)

        return list(set(calls))  # Deduplicate

    def _extract_inheritance(self, tree: ast.AST) -> Dict[str, List[str]]:
        """Extract class inheritance relationships."""

        inheritance = {}

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                bases = []
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        bases.append(base.id)
                inheritance[node.name] = bases

        return inheritance

    def map_dependencies(self, target_file: Path) -> Dict:
        """Map all dependencies of a target file."""

        # Analyze target file
        analysis = self.analyze_file(target_file)

        # Find all files that import target
        importers = self._find_importers(target_file)

        return {
            "target": str(target_file),
            "imports": analysis["imports"],  # What target imports
            "imported_by": importers,        # What imports target
            "function_calls": analysis["function_calls"],
            "inheritance": analysis["class_inheritance"],
            "impact_zone": self._calculate_impact_zone(target_file)
        }

    def _find_importers(self, target_file: Path) -> List[str]:
        """Find all files that import the target file."""

        importers = []
        target_module = self._file_to_module(target_file)

        for py_file in self.base_dir.rglob("*.py"):
            if py_file == target_file:
                continue

            try:
                tree = ast.parse(py_file.read_text())
                imports = self._extract_imports(tree)

                # Check if target module is imported
                for imp in imports:
                    if target_module in imp:
                        importers.append(str(py_file))
                        break
            except:
                pass

        return importers

    def _file_to_module(self, file_path: Path) -> str:
        """Convert file path to Python module name."""
        # backend/app/services/task_service.py -> app.services.task_service
        relative = file_path.relative_to(self.base_dir.parent)
        module = str(relative).replace("/", ".").replace("\\", ".").replace(".py", "")
        return module

    def _calculate_impact_zone(self, target_file: Path) -> List[str]:
        """Calculate all files potentially affected by changes to target."""

        impact = set()

        # Direct importers
        importers = self._find_importers(target_file)
        impact.update(importers)

        # Transitive importers (files that import the importers)
        for importer in importers:
            transitive = self._find_importers(Path(importer))
            impact.update(transitive)

        return sorted(list(impact))


# Usage
analyzer = DependencyAnalyzer(Path("backend"))
deps = analyzer.map_dependencies(Path("backend/app/services/task_service.py"))

print(f"File: {deps['target']}")
print(f"Imports: {', '.join(deps['imports'][:5])}...")
print(f"Imported by: {len(deps['imported_by'])} files")
print(f"Impact zone: {len(deps['impact_zone'])} files would be affected by changes")
```

### Workflow 3: Precise Rename Refactoring

**Rename Refactoring** (`scripts/precise_rename.py`):
```python
import ast
from pathlib import Path
from typing import List, Dict

class PreciseRenamer:
    """Rename symbols with surgical precision across the codebase."""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

    def rename_function(
        self,
        old_name: str,
        new_name: str,
        target_file: Path,
        scope: str = "all"  # "all", "file", "module"
    ) -> Dict:
        """
        Rename a function and all its references.

        Returns: List of modified files
        """

        modifications = []

        if scope == "all":
            # Rename across entire codebase
            files_to_check = list(self.base_dir.rglob("*.py"))
        elif scope == "file":
            # Only rename in target file
            files_to_check = [target_file]
        else:  # module
            # Rename in target file's directory
            files_to_check = list(target_file.parent.rglob("*.py"))

        for file_path in files_to_check:
            try:
                content = file_path.read_text()
                tree = ast.parse(content)

                renamer = RenameVisitor(old_name, new_name)
                new_tree = renamer.visit(tree)

                if renamer.modified:
                    # Convert AST back to source code
                    new_content = ast.unparse(new_tree)

                    # Preserve original formatting where possible
                    # (ast.unparse loses some formatting)
                    new_content = self._preserve_formatting(content, new_content)

                    # Write back
                    file_path.write_text(new_content)

                    modifications.append({
                        "file": str(file_path),
                        "changes": renamer.change_count,
                        "locations": renamer.change_locations
                    })

            except Exception as e:
                print(f"Error processing {file_path}: {e}")

        return {
            "old_name": old_name,
            "new_name": new_name,
            "modified_files": modifications,
            "total_changes": sum(m["changes"] for m in modifications)
        }

    def _preserve_formatting(self, original: str, new: str) -> str:
        """Attempt to preserve original formatting."""
        # TODO: More sophisticated formatting preservation
        # For now, just use ast.unparse output
        return new


class RenameVisitor(ast.NodeTransformer):
    """AST transformer to rename a symbol."""

    def __init__(self, old_name: str, new_name: str):
        self.old_name = old_name
        self.new_name = new_name
        self.modified = False
        self.change_count = 0
        self.change_locations = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Rename function definitions."""
        if node.name == self.old_name:
            node.name = self.new_name
            self.modified = True
            self.change_count += 1
            self.change_locations.append(("definition", node.lineno))

        self.generic_visit(node)
        return node

    def visit_Name(self, node: ast.Name):
        """Rename variable/function references."""
        if node.id == self.old_name:
            node.id = self.new_name
            self.modified = True
            self.change_count += 1
            self.change_locations.append(("reference", node.lineno))

        return node

    def visit_Attribute(self, node: ast.Attribute):
        """Rename attribute access (obj.old_name -> obj.new_name)."""
        if node.attr == self.old_name:
            node.attr = self.new_name
            self.modified = True
            self.change_count += 1
            self.change_locations.append(("attribute", node.lineno))

        self.generic_visit(node)
        return node


# Usage
renamer = PreciseRenamer(Path("backend"))
result = renamer.rename_function(
    old_name="get_tasks",
    new_name="list_user_tasks",
    target_file=Path("backend/app/services/task_service.py"),
    scope="all"
)

print(f"Renamed {result['old_name']} -> {result['new_name']}")
print(f"Modified {len(result['modified_files'])} files")
print(f"Total changes: {result['total_changes']}")
for mod in result['modified_files']:
    print(f"  {mod['file']}: {mod['changes']} changes at lines {mod['locations']}")
```

### Workflow 4: Extract Function Refactoring

**Extract Function** (`scripts/extract_function.py`):
```python
import ast
from pathlib import Path

class FunctionExtractor:
    """Extract code into a new function."""

    def extract_function(
        self,
        source_file: Path,
        start_line: int,
        end_line: int,
        new_function_name: str,
        target_file: Path = None
    ) -> Dict:
        """
        Extract lines [start_line, end_line] into a new function.

        Args:
            source_file: File containing code to extract
            start_line: First line to extract (1-indexed)
            end_line: Last line to extract (inclusive, 1-indexed)
            new_function_name: Name for the new function
            target_file: Where to put new function (default: same as source)

        Returns:
            Dict with:
            - new_function: Source code of extracted function
            - modified_source: Updated source file content
            - parameters: Detected parameters for new function
            - return_value: Detected return value
        """

        # Read source file
        lines = source_file.read_text().splitlines()

        # Extract code block
        extracted_lines = lines[start_line - 1:end_line]
        extracted_code = "\n".join(extracted_lines)

        # Analyze extracted code to detect:
        # 1. Variables used (become parameters)
        # 2. Variables assigned (become return values)

        tree = ast.parse(extracted_code)
        analyzer = CodeBlockAnalyzer()
        analyzer.visit(tree)

        # Build new function
        params = ", ".join(analyzer.used_vars - analyzer.assigned_vars)
        returns = ", ".join(analyzer.assigned_vars) if analyzer.assigned_vars else "None"

        indent = self._detect_indent(extracted_lines[0])

        new_function = f"""
def {new_function_name}({params}):
    \"\"\"Extracted function.\"\"\"
{self._indent_code(extracted_code, indent)}
    return {returns}
"""

        # Replace extracted code with function call
        if analyzer.assigned_vars:
            assignments = ", ".join(analyzer.assigned_vars)
            function_call = f"{assignments} = {new_function_name}({params})"
        else:
            function_call = f"{new_function_name}({params})"

        # Modify source file
        modified_lines = (
            lines[:start_line - 1] +
            [function_call] +
            lines[end_line:]
        )

        return {
            "new_function": new_function,
            "modified_source": "\n".join(modified_lines),
            "parameters": list(analyzer.used_vars - analyzer.assigned_vars),
            "return_values": list(analyzer.assigned_vars)
        }

    def _detect_indent(self, line: str) -> str:
        """Detect indentation of a line."""
        return line[:len(line) - len(line.lstrip())]

    def _indent_code(self, code: str, base_indent: str) -> str:
        """Add additional indentation to code."""
        lines = code.splitlines()
        return "\n".join(base_indent + "    " + line for line in lines)


class CodeBlockAnalyzer(ast.NodeVisitor):
    """Analyze a code block to find used and assigned variables."""

    def __init__(self):
        self.used_vars = set()
        self.assigned_vars = set()

    def visit_Name(self, node: ast.Name):
        """Track variable usage and assignment."""
        if isinstance(node.ctx, ast.Load):
            # Variable is being read
            self.used_vars.add(node.id)
        elif isinstance(node.ctx, ast.Store):
            # Variable is being assigned
            self.assigned_vars.add(node.id)

        self.generic_visit(node)


# Usage
extractor = FunctionExtractor()
result = extractor.extract_function(
    source_file=Path("backend/app/routers/tasks.py"),
    start_line=45,
    end_line=67,
    new_function_name="validate_task_input"
)

print("New function:")
print(result["new_function"])
print("\nParameters:", result["parameters"])
print("Returns:", result["return_values"])
```

---

## Quality Standards

- **Accuracy**: 100% of references found and updated
- **Safety**: Zero test failures after refactoring
- **Speed**: Search completes in <2 seconds
- **Coverage**: Handles Python, TypeScript, JavaScript
- **Precision**: No false positives in search results

---

## Integration with IDEs

Serena can integrate with:

- **VSCode**: Via Language Server Protocol (LSP)
- **PyCharm**: Via external tools
- **Vim/Neovim**: Via LSP client
- **Command Line**: Standalone scripts

---

## Safety Checks

Before any refactoring:

- [ ] Run tests to establish baseline
- [ ] Create git branch for changes
- [ ] Analyze impact zone (which files affected)
- [ ] Preview changes before applying
- [ ] Run tests after refactoring
- [ ] Verify no new linting errors
- [ ] Check type checking still passes

---

## Common Use Cases

1. **Find all uses of a deprecated function** - Before removing it
2. **Rename a poorly-named variable** - Across entire codebase
3. **Extract duplicated code** - Into reusable function
4. **Move function to different module** - Update all imports
5. **Understand impact of API change** - Map all callers
6. **Find dead code** - Functions never called
7. **Trace data flow** - From API endpoint to database

---

## Pro Tips

- **Always run tests** after Serena makes changes
- **Use git branches** for large refactorings
- **Preview changes** before applying them
- **Start small** - Test on one file before running across codebase
- **Trust but verify** - Review Serena's changes
