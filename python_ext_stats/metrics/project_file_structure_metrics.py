"""
This module provides project file structure metrics
"""

from typing import Dict, Any, List
from pathlib import Path

from python_ext_stats.metrics.project_metrics import ProjectMetrics


class ProjectFileStructureMetrics(ProjectMetrics):
    """
    Class for project file structure metrics
    """
    def value(self, all_files: List, repo_path: Path) -> Dict[str, Any]:
        """
        Calculates all project file structure metrics and returns a dict filled with them

        Returns:
            Dict: dict of calculated project file structure metrics
        """
        result_metrics = {}

        result_metrics["Number of Files in the Project"] = len(all_files)
        result_metrics["Depth of the Project File System Tree"] = \
            self.__get_depth_of_the_project_file_system_tree(all_files, repo_path)

        return result_metrics

    def available_metrics(self) -> List[str]:
        """
        Method to present a list of avaliable Project File Structure Metrics

        Returns:
            List: a list of strings as metrics' names
        """
        return ["Number of Files in the Project",
                "Depth of the Project File System Tree"
                ]

    def __get_depth_of_the_project_file_system_tree(self, all_files: List, repo_path: Path) -> int:
        """
        Calculates depth of the repository filesystem tree

        Returns:
            int: depth of the repo tree 
        """
        return max((len(path.relative_to(repo_path).parts) for path in all_files), default=0)
