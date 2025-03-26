"""
This module provides code complexity and quality metrics tests
"""

import ast
from pathlib import Path
from typing import List
import pytest

from python_ext_stats.metrics.code_complexity_and_quality_metrics\
      import CodeComplexityAndQualityMetrics


@pytest.fixture
def sample_python_code_1() -> str:
    """
    Provides sample Python code for testing cyclomatic complexity,
    Halstead complexity, LCOM, and dead code detection.
    """
    return """
def foo(x):
    if x > 0:
        return x
    else:
        return -x

class Bar:
    def __init__(self):
        self.val = 0

    def increment(self):
        self.val += 1

    def reset(self):
        self.val = 0
"""


@pytest.fixture
def sample_python_code_2() -> str:
    """
    Provides another sample Python code with an unused function for dead code detection.
    """
    return """
def unused_function():
    pass

def used_function(x):
    return x * 2
"""


# pylint: disable=W0621
@pytest.fixture
def temp_py_files(tmp_path: Path,
                  sample_python_code_1: str,
                  sample_python_code_2: str) -> List[str]:
    """
    Creates temporary .py files with sample code for testing.
    Returns a list of file paths.
    """
    file_paths = []

    file_1 = tmp_path / "sample1.py"
    file_1.write_text(sample_python_code_1, encoding="utf-8")
    file_paths.append(str(file_1))

    file_2 = tmp_path / "sample2.py"
    file_2.write_text(sample_python_code_2, encoding="utf-8")
    file_paths.append(str(file_2))

    return file_paths


# pylint: disable=W0621
@pytest.fixture
def parsed_py_files(temp_py_files: List[str]) -> List[ast.AST]:
    """
    Parses the content of the temporary Python files and returns a list of their ASTs.
    """
    parsed_files = []
    for py_file in temp_py_files:
        with open(py_file, "r", encoding="utf-8") as f:
            code = f.read()
            parsed_files.append(ast.parse(code))
    return parsed_files


@pytest.fixture
def metrics() -> CodeComplexityAndQualityMetrics:
    """
    Provides an instance of the CodeComplexityAndQualityMetrics class.
    """
    return CodeComplexityAndQualityMetrics()


class TestCodeComplexityAndQualityMetrics:
    """
    Test suite for the CodeComplexityAndQualityMetrics class.
    """

    def test_value_method(self, metrics: CodeComplexityAndQualityMetrics, parsed_py_files:\
                           List[ast.AST], temp_py_files: List[str]) -> None:
        """
        Tests the main 'value' method to ensure it returns the expected metrics keys.
        """
        result = metrics.value(parsed_py_files, temp_py_files)
        assert "Cyclomatic Complexity" in result
        assert "Halstead Complexity" in result
        assert "LCOM" in result
        assert "Dead code: unused objects" in result

    def test_cyclomatic_complexity(self, metrics: CodeComplexityAndQualityMetrics,\
                                    temp_py_files: List[str]) -> None:
        """
        Tests the cyclomatic complexity calculation method.
        """
        complexities = metrics.\
            calculate_cyclomatic_complexity(temp_py_files)
        for file_path, data in complexities.items():
            for func_name, complexity in data.items():
                assert complexity >= 1, f"Cyclomatic complexity of\
                      {func_name} in {file_path} should be >= 1"

    def test_halstead_complexity(self, metrics: CodeComplexityAndQualityMetrics,\
                                  temp_py_files: List[str]) -> None:
        """
        Tests the Halstead complexity calculation method.
        """
        halstead_data = metrics.\
            calculate_halstead_complexity(temp_py_files)
        for file_path, metrics_dict in halstead_data.items():
            for key in ["n1", "n2", "N1", "N2"]:
                assert key in metrics_dict, f"Missing Halstead metric '{key}' in {file_path}"
                assert isinstance(metrics_dict[key], int), f"{key} should be an int"

    def test_lcom(self, metrics: CodeComplexityAndQualityMetrics,\
                   parsed_py_files: List[ast.AST]) -> None:
        """
        Tests the LCOM calculation method for the classes in the sample files.
        """
        lcom_data = metrics.\
            calculate_lcom(parsed_py_files)

        print(f">>>>>>>>>>> LCOM DATA:\n {lcom_data}")

        for class_name, data in lcom_data.items():
            assert "lcom" in data, f"Missing 'lcom' value in class {class_name}"
            assert "methods" in data, f"Missing 'methods' count in class {class_name}"
            assert "attributes" in data, f"Missing 'attributes' list in class {class_name}"
            assert data["lcom"] >= 0, "LCOM value should be >= 0"
            assert data["methods"] >= 0, "Number of methods should be >= 0"

    def test_dead_code(self, metrics: CodeComplexityAndQualityMetrics,\
                        temp_py_files: List[str]) -> None:
        """
        Tests detection of dead (unused) code in the sample files.
        """
        dead_code = metrics.\
            find_dead_code(temp_py_files)

        assert any("unused_function" in unused_item.name for unused_item in dead_code), (
            "Expected 'unused_function' to be detected as dead code."
        )
        assert  any("used_function" in unused_item.name for unused_item in dead_code), (
            "'used_function' should be detected as dead code."
        )
