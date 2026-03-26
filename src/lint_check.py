"""Quick AST-based scan for unused imports across the project."""
import ast
import os

issues = []


def check_file(path):
    with open(path, encoding="utf-8") as f:
        source = f.read()
    try:
        tree = ast.parse(source, filename=path)
    except SyntaxError as e:
        issues.append(f"{path}: SyntaxError: {e}")
        return

    imported_names = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.asname if alias.asname else alias.name.split(".")[0]
                imported_names[name] = node.lineno
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                name = alias.asname if alias.asname else alias.name
                imported_names[name] = node.lineno

    used_names = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            continue
        if isinstance(node, ast.Name):
            used_names.add(node.id)
        elif isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name):
                used_names.add(node.value.id)

    for name, lineno in imported_names.items():
        if name not in used_names and name != "*":
            issues.append(f"{path}:{lineno}: unused import '{name}'")


SKIP = {"__pycache__", ".venv", ".git", "reports"}

for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in SKIP]
    for fname in files:
        if fname.endswith(".py") and fname != "lint_check.py":
            check_file(os.path.join(root, fname))

if issues:
    for i in sorted(issues):
        print(i)
else:
    print("No unused imports found.")
