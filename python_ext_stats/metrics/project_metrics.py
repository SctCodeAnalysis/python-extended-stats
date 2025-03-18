"""
This module provides project metrics
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List

class ProjectMetrics(ABC):
    """
    Abstract class for metrics or lists of metrics
    """
    @abstractmethod
    def value(self, parsed_py_files: List) -> Dict[str, Any]:
        """
        Abstract method for a single group of metrics

        Returns:
            Dict: listed results of each metric in a groop
        """

    @abstractmethod
    def available_metrics(self) -> List[str]:
        """
        Abstract method to present a list of avaliable metrics in a certain group

        Returns:
            List: a list of strings as metrics' names
        """
