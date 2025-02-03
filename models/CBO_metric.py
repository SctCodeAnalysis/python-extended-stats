from typing import Dict, Any, List
import ast

from models.project_metrics import ProjectMetrics


class CBOMetric(ProjectMetrics):
    """
    Class for coupling between objects metric
    """
    def value(self, parsed_py_files: Dict) -> Dict[str, Any]:
        result_metrics = {}

        result_metrics["Coupling Between Objects"] = self.__count_coupling_between_objects(parsed_py_files)

        return result_metrics
    
    def __count_coupling_between_objects(self, parsed_py_files: Dict) -> Dict:
        """
        Counts CBO metric for each class in the repository as a number of used  external classes

        Returns:
            dict: classname — CBO metric.
        """
        result = {}
        for module in parsed_py_files:
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