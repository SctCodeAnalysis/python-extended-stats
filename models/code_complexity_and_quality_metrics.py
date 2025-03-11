from typing import Dict, Any, List, Set
import ast
from radon.metrics import h_visit
import vulture

from models.project_metrics import ProjectMetrics


class CodeComplexityAndQualityMetrics(ProjectMetrics):
    """
    Class for code complexity and quality metrics
    """
    def value(self, parsed_py_files: List, py_files: List) -> Dict[str, Any]:
        """
        Calculates all code complexity and quality metrics and returns a dict filled with them

        Returns:
            List: list of calculated code complexity and quality metrics
        """
        result_metrics = {}

        result_metrics["Cyclomatic Complexity"] = self.__calculate_cyclomatic_complexity(py_files)
        result_metrics["Halstead Complexity"] = self.__calculate_halstead_complexity(py_files)
        result_metrics["LCOM"] = self.__calculate_lcom(parsed_py_files)
        result_metrics["Dead code: unused objects"] = self.__find_dead_code(py_files)

        return result_metrics
    
    def __calculate_cyclomatic_complexity(self, py_files: List[str]) -> Dict[str, Dict[str, int]]:
        """
        Calculates cyclomatic complexity for each func in a Python file in the provided list.
            
        Returns:
            Dict[str, Dict[str, int]]: Dictionary where keys are filenames and values are
                                      dictionaries of {function_name: complexity}
        """
        results = {}
        
        for file_path in py_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    source_code = f.read()
                tree = ast.parse(source_code)
            except SyntaxError as e:
                print(f"Syntax error in {file_path}: {e}")
                continue
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                continue

            file_complexities = {}
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    visitor = CyclomaticComplexityVisitor()
                    visitor.visit(node)
                    file_complexities[node.name] = visitor.complexity

            results[file_path] = file_complexities
            
        return results
    
    def __calculate_halstead_complexity(self, py_files: List) -> List[Dict[str, int]]:
        """
        Calculates Halstead complexity for each py file in the repository.

        Returns:
            List[Dict]: List of dictionaries with Halstead metrics for each file.
        """
        halstead_metrics = {}
        
        for py_file in py_files:
            with open(py_file, "r", encoding="utf-8") as file:
                code = file.read()
            
            try:
                analysis = h_visit(code)
                metrics = {
                    "n1": analysis.total.h1,
                    "n2": analysis.total.h2,
                    "N1": analysis.total.N1,
                    "N2": analysis.total.N2,
                }
                halstead_metrics[py_file] = metrics
            except Exception as e:
                print(f"Error analyzing {py_file}: {str(e)}")

        return halstead_metrics

    def __calculate_lcom(self, parsed_py_files: List) -> Dict[str, Any]:
        """
        Calculates LCOM metric for each class in a presented repo based on attributes' names
        
        Returns:
            Dict:
            {
                "ClassName": {
                    "lcom": int,
                    "methods": int,
                    "attributes": List[str]
                },
                ...
            }
        """

        class _AttributeVisitor(ast.NodeVisitor):
            """
            Class redefined for attributes collection
            """
            def __init__(self):
                self.attributes: Set[str] = set()

            def visit_Attribute(self, node: ast.Attribute) -> None:
                if isinstance(node.value, ast.Name) and node.value.id == "self":
                    self.attributes.add(node.attr)
                self.generic_visit(node)

        lcom_results = {}

        for parsed_file in parsed_py_files:
            for node in ast.walk(parsed_file):
                if isinstance(node, ast.ClassDef):
                    class_name = node.name
                    methods = []

                    for child in node.body:
                        if isinstance(child, ast.FunctionDef):
                            method_name = child.name
                            visitor = _AttributeVisitor()
                            visitor.visit(child)
                            methods.append({
                                "name": method_name,
                                "attributes": visitor.attributes
                            })
                    
                    lcom = 0
                    if len(methods) > 1:
                        p = 0
                        q = 0
                        
                        for i in range(len(methods)):
                            for j in range(i + 1, len(methods)):
                                attrs_i = methods[i]["attributes"]
                                attrs_j = methods[j]["attributes"]

                                if attrs_i.isdisjoint(attrs_j):
                                    p += 1
                                else:
                                    q += 1
                        
                        lcom = p - q if p > q else 0

                    all_attributes = set()
                    for method in methods:
                        all_attributes.update(method["attributes"])
                    
                    lcom_results[class_name] = {
                        "lcom": lcom,
                        "methods": len(methods),
                        "attributes": list(all_attributes)
                    }

        return lcom_results

    def __find_dead_code(self, py_files: List) -> List:
        """
        Detects dead code for each file in a presented repo

        Returns:
            List: lines of unsued code
        """

        v = vulture.Vulture()
        v.scavenge(py_files)

        return v.get_unused_code()
    

class CyclomaticComplexityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.complexity = 1

    def visit_If(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_AsyncFor(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_With(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_AsyncWith(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        self.complexity += len(node.values) - 1
        self.generic_visit(node)

    def visit_IfExp(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_comprehension(self, node):
        self.complexity += len(node.ifs)
        self.generic_visit(node)

    def visit_Raise(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_Assert(self, node):
        self.complexity += 1
        self.generic_visit(node)
