from typing import Dict, Any, List
import ast

from models.project_metrics import ProjectMetrics


class DependencyAndCouplingMetrics(ProjectMetrics):
    """
    Class for dependency and coupling metrics
    """
    def value(self, parsed_py_files: Dict, all_files: List) -> Dict[str, Any]:
        """
        Calculates all dependency and coupling metrics and returns a dict filled with them

        Returns:
            Dict: dict of calculated dependency and coupling metrics
        """
        result_metrics = {}

        result_metrics["Number of Libraries"] = self.__count_number_of_libs(parsed_py_files)
        result_metrics["Number of Extensions in the Project"] = self.__get_all_file_extensions(all_files)

        return result_metrics
    
    def __count_number_of_libs(self, parsed_py_files: Dict) -> int:
        """
        Counts the number of unique libraries imported in the parsed Python files.

        Returns:
            int: The total number of unique libraries imported in the parsed files.
        """
        imported_libs = set()

        for tree in parsed_py_files:
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imported_libs.add(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    imported_libs.add(node.module)

        return len(imported_libs)
    
    def __get_all_file_extensions(self, all_files: List) -> set:
        """
        Retrieves all unique file extensions from the list of files.

        Returns:
            set: A set of unique file extensions from the list of files.
        """
        extensions = set()

        for file in all_files:
            if file.is_file() and file.suffix:
                extensions.add(file.suffix)
        return extensions