from typing import Dict, Any, List
import ast
from pathlib import Path

from models.project_metrics import ProjectMetrics


class ProjectFileStructureMetrics(ProjectMetrics):
    """
    Class for project file structure metrics
    """
    def value(self, all_files: List, repo_path: Path) -> Dict[str, Any]:
        result_metrics = {}

        result_metrics["Number of Files in the Project"] = len(all_files)
        result_metrics["Depth of the Project File System Tree"] = self.__get_depth_of_the_project_file_system_tree(all_files, repo_path)

        return result_metrics
    
    def __get_depth_of_the_project_file_system_tree(self, all_files: List, repo_path: Path) -> int:
        """
        Calculates depth of the repository filesystem tree

        Returns:
            int: depth of the repo tree 
        """
        return max((len(path.relative_to(repo_path).parts) for path in all_files), default=0)