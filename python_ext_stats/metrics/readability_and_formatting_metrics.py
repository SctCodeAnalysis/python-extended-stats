"""
This module provides readability and formatting metrics
"""

from typing import Dict, Any, List
import ast
from collections import defaultdict


class ReadabilityAndFormattingMetrics:
    """
    Class for readability and formatting metrics
    """
    def value(self, parsed_py_files: List, py_files: List) -> Dict[str, Any]:
        """
        Calculates all readability and formatting metrics and returns a dict filled with them

        Returns:
            Dict: dict of calculated readability and formatting metrics
        """
        result_metrics = {}

        result_metrics["Duplication Percentage"] = self.__calculate_duplication_percentage(py_files)
        result_metrics["Maximum Line Length"] = self.__calculate_maximum_line_length(py_files)
        result_metrics["Lines of Code"] = self.__count_lines_of_code(py_files)
        result_metrics["Average Line Length"] = self.__calculate_average_line_length(py_files)
        result_metrics["Average Identifier Length"] = \
            self.__calculate_average_identifier_length(parsed_py_files)
        result_metrics["Number of pass keywords"] = \
            self.__count_number_pass_keywords(parsed_py_files)

        return result_metrics

    def available_metrics(self) -> List[str]:
        """
        Method to present a list of avaliable Readability And Formatting Metrics

        Returns:
            List: a list of strings as metrics' names
        """
        return ["Duplication Percentage",
                "Maximum Line Length",
                "Lines of Code",
                "Average Line Length",
                "Average Identifier Length",
                "Number of pass keywords"
                ]

    def __calculate_duplication_percentage(self, py_files: List) -> float:
        """
        Calculates the percentage of duplicated code lines across all Python files.
        Empty lines are ignored in calculations.
        
        Returns:
            float: Duplication percentage (0-100)
        """

        code_lines_count = defaultdict(int)
        total_lines = 0
        duplicated_lines = 0

        for py_file_path in py_files:
            with open(py_file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

                lines = [line.strip() for line in lines if line.strip()]
                total_lines += len(lines)

                for line in lines:
                    code_lines_count[line] += 1

                    if code_lines_count[line] > 1:
                        duplicated_lines += 1

        if total_lines == 0:
            return 0.0

        return (duplicated_lines / total_lines) * 100

    def __calculate_maximum_line_length(self, py_files: List) -> int:
        """
        Calculates maximum line length across all Python files.
        
        Returns:
            int: max length
        """

        max_length = -1

        for py_file_path in py_files:
            with open(py_file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

                lines = [line.strip() for line in lines if line.strip()]

                for line in lines:
                    max_length = max(max_length, len(line))

        return max_length

    def __count_lines_of_code(self, py_files: List) -> int:
        """
        Calculates number of lines across all Python files.
        
        Returns:
            int: max length
        """

        lines_num = 0

        for py_file_path in py_files:
            with open(py_file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                lines_num += len(lines)

        return lines_num

    def __calculate_average_line_length(self, py_files: List) -> float:
        """
        Calculates average length of line throughout all py files in a repo
        Returns:
            float: average length
        """

        sum_len = 0
        lines_num = 0

        for py_file_path in py_files:
            with open(py_file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                sum_len += sum(len(line) - 1 for line in lines)
                lines_num += len(lines)

        return sum_len / lines_num if lines_num else 0.0

    def __calculate_average_identifier_length(self, parsed_py_files: list) -> dict:
        """
        Calculates the average length of class names, method names, and field names across 
        all parsed Python files.
        Returns:
            Dict: a dictionary with the average lengths for 'class', 'method', and 'field'.
        """
        class_names = []
        method_names = []
        field_names = []

        for parsed in parsed_py_files:
            for node in ast.walk(parsed):
                if isinstance(node, ast.ClassDef):
                    class_names.append(node.name)
                    current_methods = set()
                    current_class_fields = set()
                    current_instance_fields = set()

                    for body_node in node.body:
                        if isinstance(body_node, ast.FunctionDef):
                            method_name = body_node.name
                            current_methods.add(method_name)

                            args = body_node.args.args
                            self_arg_name = args[0].arg if args else None

                            if self_arg_name:
                                for sub_node in ast.walk(body_node):
                                    if isinstance(sub_node, ast.Assign):
                                        for target in sub_node.targets:
                                            if isinstance(target, ast.Attribute):
                                                if (isinstance(target.value, ast.Name) and
                                                    (target.value.id == self_arg_name)):
                                                    current_instance_fields.add(target.attr)

                        elif isinstance(body_node, ast.Assign):
                            for target in body_node.targets:
                                if isinstance(target, ast.Name):
                                    current_class_fields.add(target.id)

                    method_names.extend(list(current_methods))
                    all_fields = current_class_fields.union(current_instance_fields)
                    field_names.extend(list(all_fields))

        return {
            'class': sum(len(name) for name in class_names) / len(class_names) \
                if class_names else 0.0,
            'method': sum(len(m) for m in method_names) / len(method_names) \
                if method_names else 0.0,
            'field': sum(len(f) for f in field_names) / len(field_names) \
                if field_names else 0.0
        }

    def __count_number_pass_keywords(self, parsed_py_files: List) -> int:
        """
        Counts the number of pass-keywords throughout all py files
        Returns:
            int: number of keywords
        """
        pass_count = 0

        for parsed_ast in parsed_py_files:
            for node in ast.walk(parsed_ast):
                if isinstance(node, ast.Pass):
                    pass_count += 1
        return pass_count
