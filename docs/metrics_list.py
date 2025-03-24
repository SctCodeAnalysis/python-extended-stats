"""
A list of presented metrics as strings
"""

from python_ext_stats.metrics.average_based_metrics import AverageBasedMetrics
from python_ext_stats.metrics.CBO_metric import CBOMetric
from python_ext_stats.metrics.class_metrics import ClassMetrics
from python_ext_stats.metrics.code_complexity_and_quality_metrics\
    import CodeComplexityAndQualityMetrics
from python_ext_stats.metrics.code_structure_metrics import CodeStructuresMetrics
from python_ext_stats.metrics.dependency_and_coupling_metrics\
    import DependencyAndCouplingMetrics
from python_ext_stats.metrics.maintainability_metrics import MaintainabilityMetrics
from python_ext_stats.metrics.project_file_structure_metrics import ProjectFileStructureMetrics
from python_ext_stats.metrics.readability_and_formatting_metrics \
    import ReadabilityAndFormattingMetrics



metrics_list = [
    AverageBasedMetrics.available_metrics(),
    CBOMetric.available_metrics(),
    ClassMetrics.available_metrics(),
    CodeComplexityAndQualityMetrics.available_metrics(),
    CodeStructuresMetrics.available_metrics(),
    DependencyAndCouplingMetrics.available_metrics(),
    MaintainabilityMetrics.available_metrics(),
    ProjectFileStructureMetrics.available_metrics(),
    ReadabilityAndFormattingMetrics.available_metrics()
]
