"""
This module provides code complexity and quality metrics tests
"""

import ast
import os
from pathlib import Path
from typing import List
import pytest

from python_ext_stats.metrics.code_complexity_and_quality_metrics\
      import CodeComplexityAndQualityMetrics


@pytest.fixture
def sample_python_code_with_low_cohesion() -> str:
    """
    Provides sample Python code with low-cohesion class for LCOM testing.
    """
    return """
class LowCohesionExample:
    def __init__(self):
        self.a = 1
        self.b = 2
        self.c = 3
    
    def method_a(self):
        return self.a
        
    def method_b(self):
        return self.b
        
    def method_c(self):
        return self.c
        
    def method_ab(self):
        return self.a + self.b
        
    def method_unrelated(self):
        return 42
"""

@pytest.fixture
def simple_python_cyclomatic_test_file():
    """Fixture for easy cyclomatic test"""
    code = """
def complex_function(x):
    for i in range(x):
        if i % 2 == 0:
            print("even")
        elif i % 3 == 0:
            print("multiple of 3")
        else:
            print("odd")
    
    while x > 0:
        try:
            x -= 1
        except Exception:
            break
    
    return [i for i in range(10) if i > 5]
"""
    return code

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


@pytest.fixture
def temp_py_files(tmp_path: Path,
                  sample_python_code_1: str,
                  sample_python_code_2: str,
                  simple_python_cyclomatic_test_file: str,
                  sample_python_code_with_low_cohesion: str) -> List[str]:
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

    file_2 = tmp_path / "sample3.py"
    file_2.write_text(simple_python_cyclomatic_test_file, encoding="utf-8")
    file_paths.append(str(file_2))    

    file_2 = tmp_path / "sample4.py"
    file_2.write_text(sample_python_code_with_low_cohesion, encoding="utf-8")
    file_paths.append(str(file_2))  

    return file_paths

@pytest.fixture
def extended_temp_py_files(tmp_path: Path,
                         sample_python_code_1: str,
                         sample_python_code_2: str,
                         sample_python_code_with_low_cohesion: str) -> List[str]:
    """
    Creates temporary .py files with additional low-cohesion class sample.
    """
    file_paths = []
    
    file_1 = tmp_path / "sample1.py"
    file_1.write_text(sample_python_code_1, encoding="utf-8")
    file_paths.append(str(file_1))

    file_2 = tmp_path / "sample2.py"
    file_2.write_text(sample_python_code_2, encoding="utf-8")
    file_paths.append(str(file_2))

    file_3 = tmp_path / "low_cohesion.py"
    file_3.write_text(sample_python_code_with_low_cohesion, encoding="utf-8")
    file_paths.append(str(file_3))
    
    return file_paths


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
                                    temp_py_files: List[str], parsed_py_files: List) -> None:
        """
        Tests the cyclomatic complexity calculation method.
        """

        complexities = metrics.\
            calculate_cyclomatic_complexity(parsed_py_files, temp_py_files)
        for file_path, data in complexities.items():
            for func_name, complexity in data.items():
                if func_name == "complex_function":
                    assert 7 == complexity
                elif func_name == "foo":
                    assert 2 == complexity
                elif func_name == "increment":
                    assert 1 == complexity
                elif func_name == "unused_function":
                    assert 1 == complexity
                
    def test_halstead_complexity_with_expected_values(self, metrics: CodeComplexityAndQualityMetrics,
                                                    temp_py_files: List[str]) -> None:
        """
        Tests the Halstead complexity calculation method with exact expected values.
        """
        expected_values = {
            "sample1.py": {
                "n1": 3,
                "n2": 4,
                "N1": 3,
                "N2": 5
            },
            "sample2.py": {
                "n1": 1,
                "n2": 2,
                "N1": 1,
                "N2": 2
            },
            "sample3.py": {
                "n1": 4,
                "n2": 9,
                "N1": 7,
                "N2": 14
            }
        }

        halstead_data = metrics.calculate_halstead_complexity(temp_py_files[:-1])
        
        for file_path, metrics_dict in halstead_data.items():
            filename = os.path.basename(file_path)
            
            assert filename in expected_values, f"Unexpected file: {filename}"
            
            for key in ["n1", "n2", "N1", "N2"]:
                assert key in metrics_dict, f"Missing Halstead metric '{key}' in {filename}"
                assert isinstance(metrics_dict[key], int), f"{key} should be an int"
                expected = expected_values[filename][key]
                assert metrics_dict[key] == expected, (
                    f"Incorrect {key} for {filename}. "
                    f"Expected {expected}, got {metrics_dict[key]}"
                )

    def test_lcom(self, metrics: CodeComplexityAndQualityMetrics,\
                   parsed_py_files: List[ast.AST]) -> None:
        """
        Tests the LCOM calculation method for the classes in the sample files.
        """
        lcom_data = metrics.\
            calculate_lcom(parsed_py_files)

        for class_name, data in lcom_data.items():
            assert "lcom" in data, f"Missing 'lcom' value in class {class_name}"
            assert "methods" in data, f"Missing 'methods' count in class {class_name}"
            assert "attributes" in data, f"Missing 'attributes' list in class {class_name}"
            assert data["lcom"] >= 0, "LCOM value should be >= 0"
            assert data["methods"] >= 0, "Number of methods should be >= 0"

    def test_lcom_with_low_cohesion_class(self, metrics: CodeComplexityAndQualityMetrics,
                                        extended_temp_py_files: List[str]) -> None:
        """
        Tests LCOM calculation with a low-cohesion class example.
        """
        parsed_files = []
        for file_path in extended_temp_py_files:
            with open(file_path, "r", encoding="utf-8") as f:
                parsed_files.append(ast.parse(f.read()))
        
        expected_values = {
            "Bar": {
                "lcom": 0,
                "methods": 3,
                "attributes": ["val"]
            },
            "LowCohesionExample": {
                "lcom": 3,
                "methods": 6,
                "attributes": ["a", "b", "c"]
            }
        }

        lcom_data = metrics.calculate_lcom(parsed_files)
        
        for class_name, expected in expected_values.items():
            actual = lcom_data[class_name]
            
            assert actual["lcom"] == expected["lcom"], (
                f"Incorrect LCOM for {class_name}. "
                f"Expected {expected['lcom']}, got {actual['lcom']}. "
                f"Full data: {actual}"
            )
            
            assert actual["methods"] == expected["methods"], (
                f"Incorrect method count for {class_name}. "
                f"Expected {expected['methods']}, got {actual['methods']}"
            )
            
            assert set(actual["attributes"]) == set(expected["attributes"]), (
                f"Incorrect attributes for {class_name}. "
                f"Expected {expected['attributes']}, got {actual['attributes']}"
            )

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
