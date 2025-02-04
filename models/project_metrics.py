from abc import ABC, abstractmethod
from typing import Dict, Any

class ProjectMetrics(ABC):
    """
    Abstract class for metrics or lists of metrics
    """
    @abstractmethod
    def value(self, parsed_py_files: Dict) -> Dict[str, Any]:
        """
        Abstract method for a single group of metrics

        Returns:
            Dict: listed results of each metric in a groop
        """
        pass