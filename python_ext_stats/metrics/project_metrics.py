"""
This module provides project metrics
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List

class ProjectMetrics(ABC):
    """
    Abstract class for metrics or lists of metrics
    """
    @classmethod
    @abstractmethod
    def value(cls, *args) -> Dict[str, Any]:
        """
        Abstract method for a single group of metrics

        Returns:
            Dict: listed results of each metric in a groop
        """

    @staticmethod
    @abstractmethod
    def available_metrics() -> List[str]:
        """
        Abstract method to present a list of avaliable metrics in a certain group

        Returns:
            List: a list of strings as metrics' names
        """
