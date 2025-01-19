from typing import List, Union

from models.metric import Metric
from docs.metrics_list import metrics_list


class ExtPythonStats:
    """
    Class for analysis based on a given repository.

    Provides metrics described in docs/metrics.tex according to the repos,
    """

    __metrics: List[str] = metrics_list.copy()

    def __init__(self, path: str):
        """
        Initiates an example of ExtPythonStats.

        Args:
            path (str): Path to the repository to analyse..
        """
        self.path = path
    
    @classmethod
    def get_metrics_list(cls) -> List[str]:
        """
        Provides a list of avaliable metrics.

        Returns:
            List[str]: A list of metrics that can be calculated.
        """
        return cls.__metrics

    def get_metric_by_name(self, metric_name: str) -> Metric:
        """
        Calculates a metrica by it's name.

        Args:
            metric_name (str): Metric's name.

        Returns:
            Union[float, int, str]: Metric's calculated value.
        """
        pass

    def get_xml_report(self) -> None:
        """
        Generates an XML report that includes all presented metrics using a given XML filename.
        
        Returns:
            None.
        """
        pass