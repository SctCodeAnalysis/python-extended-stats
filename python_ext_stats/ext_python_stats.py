"""
Module for analyzing Python repositories and generating metrics reports.
"""

from typing import List, Dict
from pathlib import Path
import ast
from datetime import datetime
import sys

import xml.etree.ElementTree as ET
import xml.dom.minidom

from python_ext_stats.metrics.project_metrics import ProjectMetrics
from python_ext_stats.metrics.code_structure_metrics import CodeStructuresMetrics
from python_ext_stats.metrics.dependency_and_coupling_metrics import (
    DependencyAndCouplingMetrics,
)
from python_ext_stats.metrics.CBO_metric import CBOMetric
from python_ext_stats.metrics.project_file_structure_metrics import (
    ProjectFileStructureMetrics,
)
from python_ext_stats.metrics.average_based_metrics import AverageBasedMetrics
from python_ext_stats.metrics.maintainability_metrics import MaintainabilityMetrics
from python_ext_stats.metrics.class_metrics import ClassMetrics
from python_ext_stats.metrics.readability_and_formatting_metrics import (
    ReadabilityAndFormattingMetrics,
)
from python_ext_stats.metrics.code_complexity_and_quality_metrics import (
    CodeComplexityAndQualityMetrics,
)

from docs.metrics_list import metrics_list
from config import VENV_DIRS


class ExtPythonStats:
    """
    Class for analysis based on a given repository.

    Provides metrics described in docs/metrics.tex according to the repos.
    """

    __metrics: List[str] = metrics_list.copy()

    def __init__(self, repo_path: str):
        """
        Initiates an example of ExtPythonStats.

        Args:
            repo_path (str): Path to the repository to analyse.
        """
        self.path = repo_path
        self.repo_path = Path(self.path)

        self.all_files = [
            f for f in self.repo_path.rglob("*")
            if not any(part in VENV_DIRS for part in f.parts)
        ]

        self.py_files = [
            f for f in self.repo_path.rglob("*.py")
            if not any(part in VENV_DIRS for part in f.parts)
        ]

        self.parsed_py_files = []

        for py_file_path in self.py_files:
            with open(py_file_path, "r", encoding="utf-8") as file:
                code = file.read()

            try:
                self.parsed_py_files.append(ast.parse(code))
            except SyntaxError:
                print(f"Unable to parse presented py file: {py_file_path}")
                sys.exit()

    @classmethod
    def get_metrics_list(cls) -> List[str]:
        """
        Provides a list of available metrics.

        Returns:
            List[str]: A list of metrics that can be calculated.
        """
        return cls.__metrics

    def get_metric_by_name(self, metric_name: str) -> ProjectMetrics:
        """
        Calculates a metric by its name.

        Args:
            metric_name (str): Metric's name.

        Returns:
            Union[float, int, str]: Metric's calculated value.
        """
        # Placeholder for metric calculation logic
        raise NotImplementedError("This method is not implemented yet.")

    def print(self, filename: str, report_data: Dict) -> None:
        """
        Generates an XML report that includes all presented metrics using a given XML filename.

        Args:
            filename (str): The name of the XML file to save the report.
            report_data (Dict): The dictionary containing the metrics data.

        Returns:
            None.
        """
        root = ET.Element("report")

        ET.SubElement(root, "report-time").text = datetime.now().strftime("%d.%m.%Y")
        ET.SubElement(root, "repository-path").text = str(self.repo_path)

        metrics_element = ET.SubElement(root, "metrics")

        for metric_name, metric_value in report_data.items():
            metric_elem = ET.SubElement(metrics_element, "metric")
            metric_elem.set("name", str(metric_name))
            metric_elem.text = str(metric_value)

        xml_str = ET.tostring(root, encoding="utf-8", xml_declaration=True)
        dom = xml.dom.minidom.parseString(xml_str)
        pretty_xml = dom.toprettyxml(indent=" ")

        with open(filename, "w", encoding="utf-8") as f:
            f.write(pretty_xml)

    def report(self) -> Dict:
        """
        Calculates the whole list of presented metrics.

        Returns:
            Dict: Metrics dict
        """
        result_metrics_dict = {}
        result_metrics_dict = {
            **result_metrics_dict,
            **CodeStructuresMetrics().value(self.parsed_py_files),
        }
        result_metrics_dict = {
            **result_metrics_dict,
            **DependencyAndCouplingMetrics().value(
                self.parsed_py_files, self.all_files
            ),
        }
        result_metrics_dict = {
            **result_metrics_dict,
            **CBOMetric().value(self.parsed_py_files),
        }
        result_metrics_dict = {
            **result_metrics_dict,
            **ProjectFileStructureMetrics().value(self.all_files, self.repo_path),
        }
        result_metrics_dict = {
            **result_metrics_dict,
            **AverageBasedMetrics().value(self.parsed_py_files, self.py_files),
        }
        result_metrics_dict = {
            **result_metrics_dict,
            **MaintainabilityMetrics().value(self.parsed_py_files),
        }
        result_metrics_dict = {
            **result_metrics_dict,
            **ClassMetrics().value(self.parsed_py_files),
        }
        result_metrics_dict = {
            **result_metrics_dict,
            **ReadabilityAndFormattingMetrics().value(
                self.parsed_py_files, self.py_files
            ),
        }
        result_metrics_dict = {
            **result_metrics_dict,
            **CodeComplexityAndQualityMetrics().value(
                self.parsed_py_files, self.py_files
            ),
        }
        return result_metrics_dict
