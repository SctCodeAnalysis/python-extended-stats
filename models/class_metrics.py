from typing import Dict, Any, List
import ast

from models.project_metrics import ProjectMetrics


class ClassMetrics(ProjectMetrics):
    """
    Class for class-metrics
    """
    def value(self, parsed_py_files: List) -> Dict[str, Any]:
        """
        Calculates all class-metrics and returns a dict filled with them

        Returns:
            Dict: dict of calculated dependency and coupling metrics
        """
        result_metrics = {}

        result_metrics["Method Hiding Factor"] = self.__calculate_method_hiding_factor(parsed_py_files)
        result_metrics["Attribute Hiding Factor"] = self.__calculate_attribute_hiding_factor(parsed_py_files)
        result_metrics["Method Inheritance Factor"] = self.__calculate_method_inheritance_factor(parsed_py_files)
        result_metrics["Polymorphism Factor"] = self.__calculate_method_polymorphism_factor(parsed_py_files)
        result_metrics["Depth Of Inheritance Tree"] = self.__calculate_depth_of_inheritance_tree(parsed_py_files)
        # result_metrics["Response for a Class"]

        return result_metrics
    
    def __calculate_method_hiding_factor(self, parsed_py_files: List) -> float:
        """
        Calculates the ratio of private methods to total methods from 0 to 1 as a float
         
        Returns:
            float: calculated method-hiding factor
        """

        private_method_num = 0
        total_method_num = 0

        for parsed_ast in parsed_py_files:
            for node in ast.walk(parsed_ast):
                if isinstance(node, (ast.ClassDef)):
                    for subnode in node.body:
                        if isinstance(subnode, ast.FunctionDef):
                            if subnode.name.startswith("_"):
                                private_method_num += 1
                            total_method_num += 1

        return private_method_num / total_method_num if total_method_num else 0

    def __calculate_attribute_hiding_factor(self, parsed_py_files: List) -> float:
        """
        Calculates  the ratio of private attributes to total attributess from 0 to 1 as a float
         
        Returns:
            float: calculated attribute-hiding factor
        """
        
        private_attr_num = 0
        total_attr_num = 0

        for parsed_ast in parsed_py_files:
            for node in ast.walk(parsed_ast):
                if isinstance(node, (ast.ClassDef)):
                    for subnode in node.body:
                        if isinstance(subnode, ast.Assign):
                            for target in subnode.targets:
                                if isinstance(target, ast.Name) and target.id.startswith("_"):
                                    private_attr_num += 1

                            total_attr_num += 1

                        elif isinstance(subnode, ast.AnnAssign):
                            if isinstance(subnode.target, ast.Name) and subnode.target.id.startswith("_"):
                                private_attr_num += 1

                            total_attr_num += 1

        return private_attr_num / total_attr_num if total_attr_num else 0.0
    
    def __calculate_method_inheritance_factor(self, parsed_py_files: List) -> Dict:
        """
        Calculates the ratio of inherited methods to total methods from 0 to 1 as a float for each class

        Returns:
            Dict: calculated ratios of inherited methods for each class 
        """

        result_inheritance = {}

        for tree in parsed_py_files:
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    inherited_methods_num = 0
                    all_methods = set()
                    
                    base_names = []
                    for base in node.bases:
                        if isinstance(base, ast.Name):
                            base_names.append(base.id)
                        elif isinstance(base, ast.Attribute):
                            base_names.append(base.attr)

                    for subnode in node.body:
                        if isinstance(subnode, ast.FunctionDef):
                            all_methods.add(subnode.name)

                    for other_node in ast.walk(tree):
                        if isinstance(other_node, ast.ClassDef) and other_node.name in base_names:
                            for subnode in other_node.body:
                                if isinstance(subnode, ast.FunctionDef):
                                    inherited_methods_num += 1
                                    all_methods.add(subnode.name)

                    result_inheritance[node.name] = (
                        inherited_methods_num / len(all_methods) 
                        if len(all_methods) > 0 
                        else 0.0
                    )

        return result_inheritance
    
    def __calculate_method_polymorphism_factor(self, parsed_py_files: List) -> Dict:
        """
        Calculates the ratio of overriden methods to total methods from 0 to 1 as a float for each class

        Returns:
            Dict: calculated ratios of overriden methods for each class 
        """
        
        result_polymorphism = {}

        for tree in parsed_py_files:
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    overriden_methods_num = 0
                    all_methods = set()
                    init_methods = []
                    
                    base_names = []
                    for base in node.bases:
                        if isinstance(base, ast.Name):
                            base_names.append(base.id)
                        elif isinstance(base, ast.Attribute):
                            base_names.append(base.attr)

                    for subnode in node.body:
                        if isinstance(subnode, ast.FunctionDef):
                            init_methods.append(subnode.name)
                            all_methods.add(subnode.name)

                    for other_node in ast.walk(tree):
                        if isinstance(other_node, ast.ClassDef) and other_node.name in base_names:
                            for subnode in other_node.body:
                                if isinstance(subnode, ast.FunctionDef):
                                    if subnode.name in init_methods:
                                        overriden_methods_num += 1
                                    all_methods.add(subnode.name)

                    if all_methods:
                        result_polymorphism[node.name] = overriden_methods_num / len(all_methods)
                    else:
                        result_polymorphism[node.name] = 0.0

        return result_polymorphism
    
    def __calculate_depth_of_inheritance_tree(self, parsed_py_files: List) -> int:
        """
        Calculates the depth of the inheritance tree by analyzing class dependencies.

        Returns:
            int: The maximum depth of inheritance tree found in the parsed code.
        """

        def get_base_name(base_node: ast.AST) -> str:
            """Gets base class name."""
            if isinstance(base_node, ast.Name):
                return base_node.id
            elif isinstance(base_node, ast.Attribute):
                return base_node.attr
            elif isinstance(base_node, ast.Call):
                return get_base_name(base_node.func)
            else:
                return "UnknownBase"

        def pseudo_dfs(temp_ver, visited, inheritance_depth, edges):
            """Calculates depth of inh. tree."""
            if visited.get(temp_ver, False):
                return

            visited[temp_ver] = True
            max_child_depth = 0

            for child in edges.get(temp_ver, []):
                if child not in visited:
                    pseudo_dfs(child, visited, inheritance_depth, edges)
                max_child_depth = max(max_child_depth, inheritance_depth.get(child, 0))

            inheritance_depth[temp_ver] = max_child_depth + 1

        edges = {}
        class_names = set()

        for module in parsed_py_files:
            for node in ast.walk(module):
                if isinstance(node, ast.ClassDef):
                    class_names.add(node.name)

        for module in parsed_py_files:
            for node in ast.walk(module):
                if isinstance(node, ast.ClassDef):
                    edges[node.name] = []
                    for base in node.bases:
                        base_name = get_base_name(base)
                        if base_name in class_names:
                            edges[node.name].append(base_name)

        inheritance_depth = {}
        visited = {cls: False for cls in edges}

        for cls in edges:
            if not visited[cls]:
                pseudo_dfs(cls, visited, inheritance_depth, edges)

        return max(inheritance_depth.values(), default=0)