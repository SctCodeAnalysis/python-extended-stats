from typing import Dict, Any, List
import ast

from models.project_metrics import ProjectMetrics


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

        result_metrics["Number of Deprecated Methods"] = self.__find_deprecated_methods(parsed_py_files)
        result_metrics["Number of Functions or Methods Without Docstrings"] = self.__count_number_of_functions_or_methods_without_docstrings(parsed_py_files)
        result_metrics["Number of Functions or Methods Without Typing"] = self.__count_number_of_functions_or_methods_without_typing(parsed_py_files)
        result_metrics["Number of Context Managers"] = self.__count_number_of_context_managers(parsed_py_files)
        result_metrics["Number of Handled Exceptions"] = self.__count_number_of_handled_exceptions(parsed_py_files)

        return result_metrics
    
    def __find_deprecated_methods(self, parsed_py_files: List) -> List: # TODO: rewrite method !!!
        """
        Finds deprecated methods

        Returns:
            list: names methods that are deprecated
        """
        pass
    
    def __count_number_of_functions_or_methods_without_docstrings(self, parsed_py_files: List) -> int:
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
    
    def __calculate_clone_coverage(self, parsed_py_files: List[ast.AST]) -> float: #TODO: reqrite methos and cope with tests
        """
        Walking through all py files, calculates clone coverage in percents
        Returns:
            float: Percentage of cloned code
        """
        class Normalizer(ast.NodeTransformer):
            def visit_FunctionDef(self, node):
                node.name = 'func'
                self.generic_visit(node)
                return node

            def visit_ClassDef(self, node):
                node.name = 'cls'
                self.generic_visit(node)
                return node

            def visit_Name(self, node):
                if isinstance(node.ctx, ast.Store):
                    node.id = 'var'
                else:
                    node.id = 'loaded_var'
                return node

            def visit_arg(self, node):
                node.arg = 'arg'
                return node

        normalized_hashes = []

        for ast_tree in parsed_py_files:
            for node in ast.walk(ast_tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    try:
                        node_dump = ast.dump(node)
                        temp_ast = ast.parse(node_dump, mode='exec')
                        temp_node = temp_ast.body[0]
                        normalized_node = Normalizer().visit(temp_node)
                        ast.fix_missing_locations(normalized_node)
                        normalized_dump = ast.dump(normalized_node, annotate_fields=False)
                        normalized_hashes.append(hash(normalized_dump))
                    except:
                        continue

        total_nodes = len(normalized_hashes)
        if total_nodes == 0:
            return 0.0

        unique_hashes = len(set(normalized_hashes))
        cloned_percent = ((total_nodes - unique_hashes) / total_nodes) * 100
        return cloned_percent