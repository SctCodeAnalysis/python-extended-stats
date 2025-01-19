from typing import Any

class Metric:
    """
    Class for a metric presentation as a result.
    """
    def __init__(self, name: str, value: Any):
        """
        Initiates an example of Metric.

        Args:
            name (str): Name of a presented metric
            value (Any): Value of a presented metric 
        """
        self.name = name
        self.value = value
