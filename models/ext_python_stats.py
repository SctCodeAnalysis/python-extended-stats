from typing import List, Union, Dict
from pathlib import Path
import ast
import json
import xml.etree.ElementTree as ET
from datetime import datetime
import xml.dom.minidom

from models.metric import Metric
from docs.metrics_list import metrics_list
from config import VENV_DIRS


class ExtPythonStats:
    """
    Class for analysis based on a given repository.

    Provides metrics described in docs/metrics.tex according to the repos,
    """

    __metrics: List[str] = metrics_list.copy()

    def __init__(self, repo_path: str):
        """
        Initiates an example of ExtPythonStats.

        Args:
            repo_path (str): Path to the repository to analyse.
        """
        self.path = repo_path
        self.repo_path = Path(self.path)

        self.all_files = list(self.repo_path.rglob("*"))
        
        self.py_files = [
            f for f in self.repo_path.rglob("*.py")
            if not any(part in VENV_DIRS for part in f.parts)
        ]

        self.parsed_py_files = []

        for py_file_path in self.py_files:
            with open(py_file_path, 'r', encoding='utf-8') as file:
                code = file.read()
            self.parsed_py_files.append(ast.parse(code))

        self.metrics_result = {}
    
    @classmethod
    def get_metrics_list(cls) -> List[str]:
        """
        Provides a list of avaliable metrics.

        Returns:
            List[str]: A list of metrics that can be calculated.
        """
        return cls.__metrics

    def get_metric_by_name(self, metric_name: str) -> Metric:
        """
        Calculates a metrica by it's name.

        Args:
            metric_name (str): Metric's name.

        Returns:
            Union[float, int, str]: Metric's calculated value.
        """
        pass

    def get_xml_report(self, filename: str) -> None:
        """
        Generates an XML report that includes all presented metrics using a given XML filename.
        
        Returns:
            None.
        """
        root = ET.Element("report")
        
        ET.SubElement(root, "report-time").text = datetime.now().strftime("%d.%m.%Y")        
        ET.SubElement(root, "repository-path").text = str(self.repo_path)
        
        metrics_element = ET.SubElement(root, "metrics")
        
        for metric_name, metric_value in self.metrics_result.items():
            metric_elem = ET.SubElement(metrics_element, "metric")
            metric_elem.set("name", str(metric_name))
            metric_elem.text = str(metric_value)
        
        xml_str = ET.tostring(root, encoding="utf-8", xml_declaration=True)
        dom = xml.dom.minidom.parseString(xml_str)
        pretty_xml = dom.toprettyxml(indent=" ")
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(pretty_xml)

    def calculate_metrics_list(self) -> None:
        """
        Calculates the whole list of presented metrics
        
        Returns:
            None.
        """
        self.metrics_result["Number of Classes"] = self.__count_number_of_classes()
        self.metrics_result["Number of Methods"] = self.__count_number_of_methods_in_classes()
        self.metrics_result["Number of Static Methods"] = self.__count_number_of_static_methods_in_classes()
        self.metrics_result["Maximum Number of Method Parameters"] = self.__count_max_number_of_method_params()
        self.metrics_result["Maximum Method Length"] = self.__count_max_method_length()
        self.metrics_result["Number of Decorators"] = self.__count_number_of_decorators()
        self.metrics_result["Number of Public Constants in File"] = self.__count_number_of_constants()
        self.metrics_result["Number of Libraries"] = self.__count_number_of_libs()
        self.metrics_result["Number of Extensions in the Project"] = self.__get_all_file_extensions()
        self.metrics_result["Coupling Between Objects"] = self.__count_coupling_between_objects()
        self.metrics_result["Number of Files in the Project"] = len(self.all_files)
        self.metrics_result["Depth of the Project File System Tree"] = self.__get_depth_of_the_project_file_system_tree()
        self.metrics_result["Average Number of Lines per File"] = self.__count_average_number_of_lines_per_file()
        self.metrics_result["Average Number of Lines per Method"] = self.__count_average_number_of_lines_per_method()
        self.metrics_result["Average Number of Methods per Class"] = self.__count_average_number_of_methods_per_class()
        self.metrics_result["Average Number of Parameters per Method or Function"] = self.__count_average_number_of_params_per_method_of_function()
        self.metrics_result["Number of deprecated methods"] = self.__find_deprecated_methods()
        self.metrics_result["Number of Functions or Methods Without Docstrings"] = self.__count_number_of_functions_or_methods_without_docstrings()
        self.metrics_result["Number of Functions or Methods Without Typing"] = self.__count_number_of_functions_or_methods_without_typing()
        self.metrics_result["Number of Context Managers"] = self.__count_number_of_context_managers()
        self.metrics_result["Number of Handled Exceptions"] = self.__count_number_of_handled_exceptions()

    def __count_number_of_classes(self) -> int:
        """
        Calculates the total number of classes in all Python files within the repository.

        Returns:
            int: The total number of classes found in all Python files.
        """
        return sum([sum(isinstance(node, ast.ClassDef) for node in ast.walk(tree)) for tree in self.parsed_py_files])
    
    def __count_number_of_methods_in_classes(self) -> int:
        """
        Counts the number of methods in all the classes across the parsed Python files.

        Returns:
            int: The total count of methods in all classes.
        """
        method_count = 0
        
        for tree in self.parsed_py_files:
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    for class_node in node.body:
                        if isinstance(class_node, ast.FunctionDef):
                            method_count += 1
        
        return method_count
    
    def __count_number_of_static_methods_in_classes(self) -> int:
        """
        Counts the number of static methods in all the classes across the parsed Python files.

        Returns:
            int: The total count of static methods across all classes.
        """
        static_methods_count = 0

        for tree in self.parsed_py_files:
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if any(isinstance(decorator, ast.Name) and decorator.id == 'staticmethod' for decorator in node.decorator_list):
                        static_methods_count += 1
        
        return static_methods_count

    def __count_max_number_of_method_params(self) -> int:
        """
        Finds the maximum number of parameters across all methods in the parsed Python files.

        Returns:
            int: The maximum number of parameters for any method in the parsed files.
        """
        max_params = 0

        for tree in self.parsed_py_files:
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    num_params = len(node.args.args)
                    max_params = max(max_params, num_params)

        return max_params

    def __count_max_method_length(self) -> int:
        """
        Finds the maximum length (in lines) of a method across all the parsed Python files.

        Returns:
            int: The maximum length (in lines) of any method in the parsed files.
        """
        max_length = 0

        for tree in self.parsed_py_files:
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if node.body:
                        start_line = node.body[0].lineno
                        end_line = node.body[-1].lineno
                        length = end_line - start_line + 1
                        max_length = max(max_length, length)

        return max_length

    def __count_number_of_decorators(self) -> int:
        """
        Counts the total number of decorators applied to functions and classes in the parsed Python files.

        Returns:
            int: The total number of decorators applied to functions and classes in the parsed files.
        """
        count = 0

        for tree in self.parsed_py_files:
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    count += len(node.decorator_list)

        return count
    
    def __count_number_of_constants(self) -> int:
        """
        Counts the total number of constants assigned in the parsed Python files.

        Returns:
            int: The total number of constants assigned in the parsed files.
        """
        constant_count = 0
        
        for tree in self.parsed_py_files:
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and isinstance(node.value, ast.Constant):
                            constant_count += 1
        
        return constant_count
    
    def __count_number_of_libs(self) -> int:
        """
        Counts the number of unique libraries imported in the parsed Python files.

        Returns:
            int: The total number of unique libraries imported in the parsed files.
        """
        imported_libs = set()

        for tree in self.parsed_py_files:
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imported_libs.add(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    imported_libs.add(node.module)

        return len(imported_libs)

    def __get_all_file_extensions(self) -> set:
        """
        Retrieves all unique file extensions from the list of files.

        Returns:
            set: A set of unique file extensions from the list of files.
        """
        extensions = set()

        for file in self.all_files:
            if file.is_file() and file.suffix:
                extensions.add(file.suffix)
        return extensions


    def __count_coupling_between_objects(self) -> Dict:
        """
        Counts CBO metric for each class in the repository as a number of used  external classes

        Returns:
            dict: classname — CBO metric.
        """
        result = {}
        for module in self.parsed_py_files:
            for node in ast.walk(module):
                if isinstance(node, ast.ClassDef):
                    class_name = node.name
                    bases_names = set()

                    for base in node.bases:
                        current = base
                        last_attr = None
                        if isinstance(current, ast.Name):
                            bases_names.add(current.id)
                        else:
                            while isinstance(current, ast.Attribute):
                                last_attr = current.attr
                                current = current.value
                            if isinstance(current, ast.Name):
                                bases_names.add(last_attr)
                    call_names = set()
                    for stmt in node.body:
                        for sub_node in ast.walk(stmt):
                            if isinstance(sub_node, ast.Call):
                                func = sub_node.func
                                if isinstance(func, ast.Name):
                                    call_names.add(func.id)
                                elif isinstance(func, ast.Attribute):
                                    current = func
                                    last_attr = None
                                    while isinstance(current, ast.Attribute):
                                        last_attr = current.attr
                                        current = current.value
                                    if last_attr:
                                        call_names.add(last_attr)
                    all_used = bases_names.union(call_names)
                    result[class_name] = len(all_used)
        return result
    
    def __get_depth_of_the_project_file_system_tree(self) -> int:
        """
        Calculates depth of the repository filesystem tree

        Returns:
            int: depth of the repo tree 
        """
        return max((len(path.relative_to(self.repo_path).parts) for path in self.all_files), default=0)
    
    def __count_average_number_of_lines_per_file(self) -> float:
        """
        Calculates average number of lines per python file

        Returns:
            float: average number 
        """
        total_lines = 0
        file_count = len(self.py_files)

        if file_count == 0:
            return 0

        for py_file_path in self.py_files:
            with open(py_file_path, 'r', encoding='utf-8') as file:
                total_lines += sum(1 for _ in file)

        return total_lines / file_count
    
    def __count_average_number_of_lines_per_method(self) -> float:
        """
        Calculates average number of lines per python method

        Returns:
            float: average number 
        """
        total_lines = 0
        total_methods = 0

        for tree in self.parsed_py_files:
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if node.body:
                        start_line = node.lineno
                        end_line = max(n.lineno for n in ast.walk(node) if hasattr(n, 'lineno'))
                        total_lines += (end_line - start_line + 1)
                        total_methods += 1

        return total_lines / total_methods if total_methods > 0 else 0
    
    def __count_average_number_of_methods_per_class(self) -> float:
        """
        Calculates average number of methods per python class

        Returns:
            float: average number 
        """
        total_methods = 0
        total_classes = 0

        for tree in self.parsed_py_files:
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    methods = sum(1 for subnode in node.body if isinstance(subnode, ast.FunctionDef))
                    total_methods += methods
                    total_classes += 1

        return total_methods / total_classes if total_classes > 0 else 0
    
    def __count_average_number_of_params_per_method_of_function(self) -> float:
        """
        Calculates average number of parameters per python method of function

        Returns:
            float: average number 
        """
        total_params = 0
        total_functions = 0

        for tree in self.parsed_py_files:
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    num_params = len(node.args.args)
                    total_params += num_params
                    total_functions += 1

        return total_params / total_functions if total_functions > 0 else 0
    
    def __find_deprecated_methods(self) -> List: # TODO: перепроверить работу метода !!!
        """
        Finds deprecated methods

        Returns:
            list: names methods that are deprecated
        """
        deprecated_methods = []

        for tree in self.parsed_py_files:
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if any(isinstance(decorator, ast.Name) and decorator.id == 'deprecated' for decorator in node.decorator_list):
                        deprecated_methods.append(node.name)

                if isinstance(node, ast.ClassDef):
                    for subnode in node.body:
                        if isinstance(subnode, ast.FunctionDef):
                            if any(isinstance(decorator, ast.Name) and decorator.id == 'deprecated' for decorator in subnode.decorator_list):
                                deprecated_methods.append(f"{node.name}.{subnode.name}")

        return deprecated_methods

    def __count_number_of_functions_or_methods_without_docstrings(self) -> int:
        """
        Walks all methods and functions and counts the number of those that have no docstring

        Returns: 
            int: Number of Functions or Methods Without Docstrings
        """
        counter = 0

        for parsed_ast in self.parsed_py_files:
            for node in ast.walk(parsed_ast):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if not ast.get_docstring(node):
                        counter += 1
        return counter

    def __count_number_of_functions_or_methods_without_typing(self) -> int:
        """
        Walks all methods and functions and counts those that have no typing used in them
        
        Returns:
            int: Number of Functions or Methods Without Typing
        """
        count = 0

        for parsed_ast in self.parsed_py_files:
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
    
    def __count_number_of_context_managers(self) -> int:
        """
        Calculates a number of context managers in python files

        Returns:
            int: Context Managers number
        
        """
        context_manager_count = 0

        for parsed_ast in self.parsed_py_files:
            for node in ast.walk(parsed_ast):
                if isinstance(node, ast.With):
                    context_manager_count += len(node.items)

        return context_manager_count
    
    def __count_number_of_handled_exceptions(self) -> int: 
        """
        Walking through all py files, counts the number of handled exceptions

        Returns:
            int: Number of handled exceptions
        """
        handled_exceptions = set()

        for tree in self.parsed_py_files:
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