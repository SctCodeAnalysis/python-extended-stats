from typing import Dict, Any, List
import ast

from models.project_metrics import ProjectMetrics


class CodeStructuresMetrics(ProjectMetrics):
    """
    Class for code structure metrics
    """
    def value(self, parsed_py_files: List) -> Dict[str, Any]:
        """
        Calculates all code ctructures metrics and returns a dict filled with them

        Returns:
            Dict: dict of calculated code structures metrics
        """
        result_metrics = {}

        result_metrics["Number of Classes"] = self.__count_number_of_classes(parsed_py_files)
        result_metrics["Number of Methods"] = self.__count_number_of_methods_in_classes(parsed_py_files)
        result_metrics["Number of Static Methods"] = self.__count_number_of_static_methods_in_classes(parsed_py_files)
        result_metrics["Maximum Number of Method Parameters"] = self.__count_max_number_of_method_params(parsed_py_files)
        result_metrics["Maximum Method Length"] = self.__count_max_method_length(parsed_py_files)
        result_metrics["Number of Decorators"] = self.__count_number_of_decorators(parsed_py_files)
        result_metrics["Number of Public Constants in File"] = self.__count_number_of_constants(parsed_py_files)

        return result_metrics

    def __count_number_of_classes(self, parsed_py_files: Dict) -> int:
        """
        Calculates the total number of classes in all Python files within the repository.

        Returns:
            int: The total number of classes found in all Python files.
        """
        return sum([sum(isinstance(node, ast.ClassDef) for node in ast.walk(tree)) for tree in parsed_py_files])

    def __count_number_of_methods_in_classes(self, parsed_py_files: Dict) -> int:
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
    
    def __count_number_of_static_methods_in_classes(self, parsed_py_files: Dict) -> int:
        """
        Counts the number of static methods in all the classes across the parsed Python files.

        Returns:
            int: The total count of static methods across all classes.
        """
        static_methods_count = 0

        for tree in parsed_py_files:
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if any(isinstance(decorator, ast.Name) and decorator.id == 'staticmethod' for decorator in node.decorator_list):
                        static_methods_count += 1
        
        return static_methods_count
    
    def __count_max_number_of_method_params(self, parsed_py_files: Dict) -> int:
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
    
    def __count_max_method_length(self, parsed_py_files: Dict) -> int:
        """
        Finds the maximum length (in lines) of a method across all the parsed Python files.

        Returns:
            int: The maximum length (in lines) of any method in the parsed files.
        """
        max_length = 0

        for tree in parsed_py_files:
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if node.body:
                        start_line = node.body[0].lineno
                        end_line = node.body[-1].lineno
                        length = end_line - start_line + 1
                        max_length = max(max_length, length)

        return max_length
    
    def __count_number_of_decorators(self, parsed_py_files: Dict) -> int:
        """
        Counts the total number of decorators applied to functions and classes in the parsed Python files.

        Returns:
            int: The total number of decorators applied to functions and classes in the parsed files.
        """
        count = 0

        for tree in parsed_py_files:
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    count += len(node.decorator_list)

        return count
    
    def __count_number_of_constants(self, parsed_py_files: Dict) -> int:
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