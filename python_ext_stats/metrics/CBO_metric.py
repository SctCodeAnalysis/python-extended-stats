"""
This module provides class-based CBO metric
"""

from typing import Dict, Any, List
import ast

from python_ext_stats.metrics.project_metrics import ProjectMetrics


class CBOMetric(ProjectMetrics):
    """
    Class for coupling between objects metric
    """
    def value(self, parsed_py_files: List) -> Dict[str, Any]:
        """
        Calculates CBO metric and returns a list filled with it

        Returns:
            List: list of calculated CBO metric
        """
        result_metrics = {}

        result_metrics["Coupling Between Objects"] = \
            self.__count_coupling_between_objects(parsed_py_files)
        return result_metrics

    def available_metrics(self) -> List[str]:
        """
        Method to present a list of a CBO metric

        Returns:
            List: a list of strings as metric's name
        """
        return ["Coupling between objects"]

    def __count_coupling_between_objects(self, parsed_py_files: List) -> Dict:
        """
        Counts CBO metric, ignoring method calls via object attributes.
        """
        result = {}
        builtins = {'int', 'str', 'list', 'dict', 'bool', 'float'}

        for module in parsed_py_files:
            module_classes = set()
            for node in ast.walk(module):
                if isinstance(node, ast.ClassDef):
                    module_classes.add(node.name)

            for node in ast.walk(module):
                if isinstance(node, ast.ClassDef):
                    class_name = node.name
                    bases_names = set()

                    for base in node.bases:
                        current = base
                        parts = []
                        while isinstance(current, ast.Attribute):
                            parts.append(current.attr)
                            current = current.value
                        if isinstance(current, ast.Name):
                            parts.append(current.id)
                            base_class = '.'.join(reversed(parts))
                            if base_class not in builtins:
                                bases_names.add(base_class)

                    call_names = set()
                    for stmt in node.body:
                        for sub_node in ast.walk(stmt):
                            if isinstance(sub_node, ast.Call):
                                func = sub_node.func

                                if isinstance(func, ast.Name):
                                    if func.id not in builtins:
                                        call_names.add(func.id)

                                elif isinstance(func, ast.Attribute):
                                    current = func
                                    parts = []
                                    while isinstance(current, ast.Attribute):
                                        parts.append(current.attr)
                                        current = current.value
                                    if isinstance(current, ast.Name):
                                        parts.append(current.id)
                                        full_name = '.'.join(reversed(parts))
                                        if full_name in module_classes \
                                            and full_name not in builtins:
                                            call_names.add(full_name)

                    all_used = bases_names.union(call_names)
                    result[class_name] = len(all_used)

        return result
