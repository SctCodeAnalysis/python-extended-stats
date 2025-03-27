"""Module for calculating average-based metrics in Python projects."""

from typing import Dict, Any, List
from pathlib import Path
import ast

from python_ext_stats.metrics.project_metrics import ProjectMetrics


class AverageBasedMetrics(ProjectMetrics):
    """
    Class for average-based metrics
    """
    @classmethod
    def value(cls, parsed_py_files: List = None, py_files: List = None,
              all_files: List = None, repo_path: Path = None) -> Dict[str, Any]:
        """
        Calculates all average-based metrics and returns a list filled with them

        Returns:
            List: list of calculated average-based metrics
        """
        result_metrics = {}

        result_metrics["Average Number of Lines per File"] = \
            cls.count_average_number_of_lines_per_file(py_files)
        result_metrics["Average Number of Lines per Method"] = \
            cls.count_average_number_of_lines_per_method(parsed_py_files)
        result_metrics["Average Number of Methods per Class"] =  \
            cls.count_average_number_of_methods_per_class(parsed_py_files)
        result_metrics["Average Number of Parameters per Method/Function"] = \
            cls.count_average_number_of_params_per_method_or_function(
                parsed_py_files)

        return result_metrics
    @staticmethod
    def available_metrics() -> List[str]:
        """
        Method to present a list of avaliable average based metrics

        Returns:
            List: a list of strings as metrics' names
        """
        return [
            "Average Number of Lines per File",
            "Average Number of Lines per Method",
            "Average Number of Methods per Class",
            "Average Number of Parameters per Method/Function"
        ]

    @staticmethod
    def count_average_number_of_lines_per_file(py_files: List) -> float:
        """
        Calculates average number of lines per python file

        Returns:
            float: average number
        """
        total_lines = 0
        file_count = len(py_files)

        if file_count == 0:
            return 0

        for py_file_path in py_files:
            with open(py_file_path, 'r', encoding='utf-8') as file:
                total_lines += sum(1 for _ in file)

        return total_lines / file_count

    @staticmethod
    def count_average_number_of_lines_per_method(parsed_py_files: List) -> float:
        """
        Calculates average number of lines per python method

        Returns:
            float: average number
        """
        total_lines = 0
        total_methods = 0

        for tree in parsed_py_files:
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if node.body:
                        start_line = node.lineno
                        end_line = max(
                            n.lineno for n in ast.walk(node)
                            if hasattr(n, 'lineno')
                        )
                        total_lines += (end_line - start_line)
                        total_methods += 1

        return total_lines / total_methods if total_methods > 0 else 0

    @staticmethod
    def count_average_number_of_methods_per_class(parsed_py_files: List) -> float:
        """
        Calculates average number of methods per python class

        Returns:
            float: average number
        """
        total_methods = 0
        total_classes = 0

        for tree in parsed_py_files:
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    methods = sum(
                        1 for subnode in node.body
                        if isinstance(subnode, ast.FunctionDef)
                    )
                    total_methods += methods
                    total_classes += 1

        return total_methods / total_classes if total_classes > 0 else 0

    @staticmethod
    def count_average_number_of_params_per_method_or_function(parsed_py_files: List)\
          -> float:
        """
        Calculates average number of parameters per python method or function

        Returns:
            float: average number
        """
        total_params = 0
        total_functions = 0

        for tree in parsed_py_files:
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    num_params = len(node.args.args)
                    total_params += num_params
                    total_functions += 1

        return total_params / total_functions if total_functions > 0 else 0
