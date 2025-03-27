"""
This module privedes specific code complexity and quality netrics
"""

from typing import Dict, Any, List, Set
from pathlib import Path
import ast
import sys
from radon.visitors import HalsteadVisitor
import vulture

from python_ext_stats.metrics.project_metrics import ProjectMetrics


class CodeComplexityAndQualityMetrics(ProjectMetrics):
    """
    Class for code complexity and quality metrics
    """
    @classmethod
    def value(cls, parsed_py_files: List = None, py_files: List = None,
              all_files: List = None, repo_path: Path = None) -> Dict[str, Any]:
        """
        Calculates all code complexity and quality metrics and returns a dict filled with them

        Returns:
            List: list of calculated code complexity and quality metrics
        """
        result_metrics = {}

        result_metrics["Cyclomatic Complexity"] = cls.calculate_cyclomatic_complexity(py_files)
        result_metrics["Halstead Complexity"] = cls.calculate_halstead_complexity(py_files)
        result_metrics["LCOM"] = cls.calculate_lcom(parsed_py_files)
        result_metrics["Dead code: unused objects"] = cls.find_dead_code(py_files)

        return result_metrics

    @staticmethod
    def available_metrics() -> List[str]:
        """
        Method to present a list of avaliable Code Complexity And Quality Metrics

        Returns:
            List: a list of strings as metrics' names
        """
        return ["Cyclomatic Complexity",
                "Halstead Complexity",
                "LCOM",
                "Dead code: unused objects"
                ]

    @staticmethod
    def calculate_cyclomatic_complexity(py_files: List[str]) -> Dict[str, Dict[str, int]]:
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

            file_complexities = {}

            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    visitor = CyclomaticComplexityVisitor()
                    try:
                        visitor.visit(node)
                    except RecursionError:
                        print("ERROR RECURSION in ", file_path)
                        sys.exit()
                    file_complexities[node.name] = visitor.complexity

            results[file_path] = file_complexities

        return results

    @staticmethod
    def calculate_halstead_complexity(py_files: List) -> List[Dict[str, int]]:
        """
        Calculates Halstead complexity for each py file in the repository.

        Returns:
            List[Dict]: List of dictionaries with Halstead metrics for each file.
        """
        halstead_metrics = {}

        for py_file in py_files:
            with open(py_file, "r", encoding="utf-8") as file:
                code = file.read()

            visitor = HalsteadVisitor.from_code(code)
            metrics = {
                "n1": visitor.distinct_operators,
                "n2": visitor.distinct_operands,
                "N1": visitor.operators,
                "N2": visitor.operands
            }
            halstead_metrics[py_file] = metrics

        return halstead_metrics

    @staticmethod
    def calculate_lcom(parsed_py_files: List) -> Dict[str, Any]:
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
                """
                subclass init
                """
                self.attributes: Set[str] = set()

            # pylint: disable=C0103
            def visit_Attribute(self, node: ast.Attribute) -> None:
                """
                method to specify behaviour while visiting an Attribute
                """
                if isinstance(node.value, ast.Name) and node.value.id == "self":
                    self.attributes.add(node.attr)
                self.generic_visit(node)
            
            def visit_Assign(self, node: ast.Assign) -> None:
                for target in node.targets:
                    if isinstance(target, ast.Attribute):
                        if isinstance(target.value, ast.Name) and target.value.id == "self":
                            self.attributes.add(target.attr)
                self.generic_visit(node)

        def run_methods_lcom(methods):
            lcom = 0
            if len(methods) > 1:
                p = 0
                q = 0

                len_m = len(methods)

                for i in range(len_m):
                    for j in range(i + 1, len(methods)):
                        attrs_i = methods[i]["attributes"]
                        attrs_j = methods[j]["attributes"]

                        if attrs_i.isdisjoint(attrs_j):
                            p += 1
                        else:
                            q += 1

                lcom = p - q if p > q else 0
            return lcom

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

                    lcom = run_methods_lcom(methods)

                    all_attributes = set()
                    for method in methods:
                        all_attributes.update(method["attributes"])

                    lcom_results[class_name] = {
                        "lcom": lcom,
                        "methods": len(methods),
                        "attributes": list(all_attributes)
                    }

        return lcom_results

    @staticmethod
    def find_dead_code(py_files: List) -> List:
        """
        Detects dead code for each file in a presented repo

        Returns:
            List: pieces of unsued code
        """

        v = vulture.Vulture()
        v.scavenge(py_files)

        return v.get_unused_code()


class CyclomaticComplexityVisitor(ast.NodeVisitor):
    """
    Specific class that describes behavour in a certain node
    """
    def __init__(self):
        """
        class init
        """
        self.complexity = 1

    def visit_If(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_Else(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node):
        """
        method to visit FOR
        """
        self.complexity += 1
        self.generic_visit(node)

    def visit_AsyncFor(self, node):
        """
        method to visit ASYNCFOR
        """
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node):
        """
        method to visit WHILE
        """
        self.complexity += 1
        self.generic_visit(node)

    def visit_With(self, node):
        """
        method to visit WITH
        """
        self.complexity += 1
        self.generic_visit(node)

    def visit_AsyncWith(self, node):
        """
        method to visit AsyncWith
        """
        self.complexity += 1
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        """
        method to visit EXCEPTHANDLER
        """
        self.complexity += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        """
        method to visit BOOL OP.
        """
        self.complexity += len(node.values) - 1
        self.generic_visit(node)

    def visit_IfExp(self, node):
        """
        method to visit IFExp
        """
        self.complexity += 1
        self.generic_visit(node)

    def visit_comprehension(self, node):
        """
        method to visit comprehension
        """
        self.complexity += len(node.ifs)
        self.generic_visit(node)

    def visit_Raise(self, node):
        """
        method to visit RAISE
        """
        self.complexity += 1
        self.generic_visit(node)

    def visit_Assert(self, node):
        """
        method to visit ASSERT
        """
        self.complexity += 1
        self.generic_visit(node)
