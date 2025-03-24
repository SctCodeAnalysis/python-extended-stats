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

    @classmethod
    def value(cls, parsed_py_files: List) -> Dict[str, Any]:
        """
        Calculates CBO metric and returns a list filled with it

        Returns:
            List: list of calculated CBO metric
        """
        result_metrics = {}

        result_metrics["Coupling Between Objects"] = \
            cls.count_coupling_between_objects(parsed_py_files)
        return result_metrics

    @staticmethod
    def available_metrics() -> List[str]:
        """
        Method to present a list of a CBO metric

        Returns:
            List: a list of strings as metric's name
        """
        return ["Coupling between objects"]

    @staticmethod
    def count_coupling_between_objects(parsed_py_files: List) -> Dict:
        """
        Counts CBO metric, ignoring method calls via object attributes.
        """

        def add_module_classes(module):
            module_classes = set()
            for node in ast.walk(module):
                if isinstance(node, ast.ClassDef):
                    module_classes.add(node.name)
            return module_classes

        def add_bases_names(node):
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
            return bases_names

        def add_call_names_for_attr(call_names, func):
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

        def walk_module(module, result, builtins):
            def add_call_names(func, call_names, builtins):
                if isinstance(func, ast.Name):
                    if func.id not in builtins:
                        call_names.add(func.id)

                elif isinstance(func, ast.Attribute):
                    add_call_names_for_attr(call_names, func)

            for node in ast.walk(module):
                if isinstance(node, ast.ClassDef):
                    class_name = node.name
                    bases_names = add_bases_names(node)

                    call_names = set()
                    for stmt in node.body:
                        for sub_node in ast.walk(stmt):
                            if isinstance(sub_node, ast.Call):
                                func = sub_node.func

                                add_call_names(func, call_names, builtins)

                    all_used = bases_names.union(call_names)
                    result[class_name] = len(all_used)

        result = {}
        builtins = {'int', 'str', 'list', 'dict', 'bool', 'float'}

        for module in parsed_py_files:
            module_classes = add_module_classes(module)

            walk_module(module, result, builtins)

        return result
