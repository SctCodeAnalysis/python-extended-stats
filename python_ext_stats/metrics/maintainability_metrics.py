"""
Module that provides maintainability metrics
"""

from typing import Dict, Any, List
import ast

from python_ext_stats.metrics.project_metrics import ProjectMetrics


class MaintainabilityMetrics(ProjectMetrics):
    """
    Class for maintainability metrics
    """
    def value(self, parsed_py_files: List) -> Dict[str, Any]:
        """
        Calculates all maintainability metrics and returns a dict filled with them

        Returns:
            Dict: dict of calculated dependency and coupling metrics
        """
        result_metrics = {}

        result_metrics["Number of Functions or Methods Without Docstrings"] = \
            self.__count_number_of_functions_or_methods_without_docstrings(parsed_py_files)
        result_metrics["Number of Functions or Methods Without Typing"] = \
            self.__count_number_of_functions_or_methods_without_typing(parsed_py_files)
        result_metrics["Number of Context Managers"] = \
            self.__count_number_of_context_managers(parsed_py_files)
        result_metrics["Number of Handled Exceptions"] = \
            self.__count_number_of_handled_exceptions(parsed_py_files)

        return result_metrics

    def available_metrics(self) -> List[str]:
        """
        Method to present a list of avaliable Maintainability Metrics

        Returns:
            List: a list of strings as metrics' names
        """
        return ["Number of Deprecated Methods",
                "Number of Functions or Methods Without Docstrings",
                "Number of Functions or Methods Without Typing",
                "Number of Context Managers",
                "Number of Handled Exceptions"
                ]

    def __count_number_of_functions_or_methods_without_docstrings\
        (self, parsed_py_files: List) -> int:
        """
        Walks all methods and functions and counts the number of those that have no docstring

        Returns: 
            int: Number of Functions or Methods Without Docstrings
        """
        counter = 0

        for parsed_ast in parsed_py_files:
            for node in ast.walk(parsed_ast):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if not ast.get_docstring(node):
                        counter += 1
        return counter

    def __count_number_of_functions_or_methods_without_typing(self, parsed_py_files: List) -> int:
        """
        Walks all methods and functions and counts those that have no typing used in them
        
        Returns:
            int: Number of Functions or Methods Without Typing
        """
        count = 0

        for parsed_ast in parsed_py_files:
            for node in ast.walk(parsed_ast):
                if isinstance(node, ast.FunctionDef):
                    has_typing = True

                    args = node.args
                    all_args = (
                        args.posonlyargs
                        + args.args
                        + ([] if args.vararg is None else [args.vararg])  # *args
                        + args.kwonlyargs
                        + ([] if args.kwarg is None else [args.kwarg])     # **kwargs
                    )

                    for arg in all_args:
                        if arg.annotation is None:
                            has_typing = False
                            break

                    if node.returns is None:
                        has_typing = False

                    if not has_typing:
                        count += 1

        return count

    def __count_number_of_context_managers(self, parsed_py_files: List) -> int:
        """
        Calculates a number of context managers in python files

        Returns:
            int: Context Managers number
        
        """
        context_manager_count = 0

        for parsed_ast in parsed_py_files:
            for node in ast.walk(parsed_ast):
                if isinstance(node, ast.With):
                    context_manager_count += len(node.items)

        return context_manager_count

    def __count_number_of_handled_exceptions(self, parsed_py_files: List) -> int:
        """
        Walking through all py files, counts the number of handled exceptions

        Returns:
            int: Number of handled exceptions
        """
        handled_exceptions = set()

        for tree in parsed_py_files:
            for node in ast.walk(tree):
                if isinstance(node, ast.Try):
                    for handler in node.handlers:
                        if handler.type:
                            if isinstance(handler.type, ast.Tuple):
                                for exc in handler.type.elts:
                                    handled_exceptions.add(ast.unparse(exc).strip())
                            else:
                                handled_exceptions.add(ast.unparse(handler.type).strip())

        return len(handled_exceptions)
