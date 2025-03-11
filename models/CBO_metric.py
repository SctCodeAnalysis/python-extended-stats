from typing import Dict, Any, List, Set
import ast

from models.project_metrics import ProjectMetrics


class CBOMetric(ProjectMetrics):
    """
    Class for coupling between objects metric
    """
    def value(self, parsed_py_files: List) -> Dict[str, Any]:
        """
        CBO metric preparing method that converts calculations into a presentative response dict
        """
        return {
            "Coupling Between Objects": self.__count_coupling_between_objects(parsed_py_files)
        }
    
    def __count_coupling_between_objects(self, parsed_py_files: List) -> Dict:
        """
        Calculates CBO metric for the listed py files
        """
        result = {}
        builtins = self.__get_builtin_types()
        
        for module in parsed_py_files:
            module_classes = self.__get_module_classes(module)
            for node in ast.walk(module):
                if isinstance(node, ast.ClassDef):
                    class_name = node.name
                    bases = self.__get_base_classes(node.bases, module_classes, builtins)
                    calls = self.__get_method_calls(node.body, module_classes, builtins)
                    result[class_name] = len(bases.union(calls))
        
        return result

    def __get_builtin_types(self) -> Set[str]:
        """
        Returns a list of builtin types
        """
        return {'int', 'str', 'list', 'dict', 'bool', 'float'}

    def __get_module_classes(self, module: ast.Module) -> Set[str]:
        """
        List all ClassNames across a presented module
        """
        return {n.name for n in ast.walk(module) if isinstance(n, ast.ClassDef)}

    def __get_base_classes(self, bases: List[ast.expr], module_classes: Set[str], builtins: Set[str]) -> Set[str]:
        """
        Collect base classes from the list
        """
        base_classes = set()
        
        for base in bases:
            if (class_name := self.__extract_entity_name(base)) \
                and class_name not in builtins:
                base_classes.add(class_name)
        
        return base_classes

    def __get_method_calls(self, body: List[ast.stmt], module_classes: Set[str], builtins: Set[str]) -> Set[str]:
        """
        Collect calls
        """
        called_classes = set()
        
        for stmt in body:
            for sub_node in ast.walk(stmt):
                if isinstance(sub_node, ast.Call) \
                    and (class_name := self.__extract_entity_name(sub_node.func, module_classes)):
                    called_classes.add(class_name)
        
        return called_classes

    def __extract_entity_name(self, node: ast.expr, module_classes: Set[str] = None) -> str:
        """
        Get name of a presented node
        """
        if isinstance(node, ast.Name):
            return node.id
        
        if isinstance(node, ast.Attribute):
            parts = []
            current = node
            while isinstance(current, ast.Attribute):
                parts.append(current.attr)
                current = current.value
            
            if isinstance(current, ast.Name):
                parts.append(current.id)
                full_name = '.'.join(reversed(parts))
                if module_classes is None or full_name in module_classes:
                    return full_name
        
        return None