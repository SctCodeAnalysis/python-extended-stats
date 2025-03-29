"""
Module that specifies code structure metrics
"""
from typing import Dict, Any, List
from pathlib import Path
import ast

from python_ext_stats.metrics.project_metrics import ProjectMetrics


class CodeStructuresMetrics(ProjectMetrics):
    """
    Class for code structure metrics
    """
    @classmethod
    def value(cls, parsed_py_files: List = None, py_files: List = None,
              all_files: List = None, repo_path: Path = None) -> Dict[str, Any]:
        """
        Calculates all code ctructures metrics and returns a dict filled with them

        Returns:
            Dict: dict of calculated code structures metrics
        """
        result_metrics = {}

        result_metrics["Number of Classes"] = cls.count_number_of_classes(parsed_py_files)
        result_metrics["Number of Methods"] = \
            cls.count_number_of_methods_in_classes(parsed_py_files)
        result_metrics["Number of Static Methods"] = \
            cls.count_number_of_static_methods_in_classes(parsed_py_files)
        result_metrics["Maximum Number of Method Parameters"] = \
            cls.count_max_number_of_method_params(parsed_py_files)
        result_metrics["Maximum Method Length"] = \
            cls.count_max_method_length(parsed_py_files)
        result_metrics["Number of Decorators"] = \
            cls.count_number_of_decorators(parsed_py_files)
        result_metrics["Number of Public Constants in File"] = \
            cls.count_number_of_constants(parsed_py_files)

        return result_metrics

    @staticmethod
    def available_metrics() -> List[str]:
        """
        Method to present a list of avaliable code structure metrics

        Returns:
            List: a list of strings as metrics' names
        """
        return ["Number of Classes",
                "Number of Methods",
                "Number of Static Methods",
                "Maximum Number of Method Parameters",
                "Maximum Method Length",
                "Number of Decorators",
                "Number of Public Constants in File"
                ]

    @staticmethod
    def count_number_of_classes(parsed_py_files: Dict) -> int:
        """
        Calculates the total number of classes in all Python files within the repository.

        Returns:
            int: The total number of classes found in all Python files.
        """
        return sum(
            isinstance(node, ast.ClassDef)
            for tree in parsed_py_files
            for node in ast.walk(tree)
        )

    @staticmethod
    def count_number_of_methods_in_classes(parsed_py_files: Dict) -> int:
        """
        Counts the number of methods in all the classes across the parsed Python files.

        Returns:
            int: The total count of methods in all classes.
        """
        method_count = 0

        for tree in parsed_py_files:
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    for class_node in node.body:
                        if isinstance(class_node, ast.FunctionDef):
                            method_count += 1

        return method_count

    @staticmethod
    def count_number_of_static_methods_in_classes(parsed_py_files: Dict) -> int:
        """
        Counts the number of static methods in all the classes across the parsed Python files.

        Returns:
            int: The total count of static methods across all classes.
        """
        static_methods_count = 0

        for tree in parsed_py_files:
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if any(isinstance(decorator, ast.Name) and decorator.id == 'staticmethod'\
                            for decorator in node.decorator_list):
                        static_methods_count += 1

        return static_methods_count

    @staticmethod
    def count_max_number_of_method_params(parsed_py_files: Dict) -> int:
        """
        Finds the maximum number of parameters across all methods in the parsed Python files.

        Returns:
            int: The maximum number of parameters for any method in the parsed files.
        """
        max_params = 0

        for tree in parsed_py_files:
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    num_params = len(node.args.args)
                    max_params = max(max_params, num_params)

        return max_params

    @staticmethod
    def count_max_method_length(parsed_py_files: List) -> int:
        """
        Counts max method length across all py files
        """
        max_length = 0

        for tree in parsed_py_files:
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    try:
                        start_line = node.lineno
                        if hasattr(node, 'end_lineno'):
                            end_line = node.end_lineno
                        else:
                            end_line = start_line

                        method_length = end_line - start_line
                        max_length = max(max_length, method_length)

                    except AttributeError as e:
                        print(f"Error processing method: {e}")
                        continue

        return max_length

    @staticmethod
    def count_number_of_decorators(parsed_py_files: Dict) -> int:
        """
        Counts the total number of decorators applied to functions
        and classes in the parsed Python files.

        Returns:
            int: The total number of decorators applied to functions
                 and classes in the parsed files.
        """
        count = 0

        for tree in parsed_py_files:
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    count += len(node.decorator_list)

        return count

    @staticmethod
    def count_number_of_constants(parsed_py_files: Dict) -> int:
        """
        Counts the total number of constants assigned in the parsed Python files.

        Returns:
            int: The total number of constants assigned in the parsed files.
        """
        constant_count = 0

        for tree in parsed_py_files:
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and isinstance(node.value, ast.Constant):
                            constant_count += 1

        return constant_count
