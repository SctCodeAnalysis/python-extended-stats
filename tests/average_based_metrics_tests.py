"""
This module provides average based metrics tests
"""

import sys
from pathlib import Path
import ast
import pytest

from python_ext_stats.metrics.average_based_metrics import AverageBasedMetrics


PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))



@pytest.fixture
def metrics():
    """
    Fixture to initialize an instance of AverageBasedMetrics.
    """
    return AverageBasedMetrics()

@pytest.fixture
def empty_file_list():
    """Fixture for an empty list of files."""
    return []

@pytest.fixture
def multiple_files(tmp_path):
    """Fixture for multiple files with varying line counts."""
    file1 = tmp_path / "file1.py"
    file1.write_text("a = 1\nb = 2\nc = 3")

    file2 = tmp_path / "file2.py"
    file2.write_text("x = 4\ny = 5\nz = 6\nw = 7\nv = 8")

    return [file1, file2]

@pytest.fixture
def methods_code():
    """Fixture for code containing multiple methods."""
    return """
def method1():
    a = 1
    b = 2
    c = 3

def method2():
    x = 4
"""

@pytest.fixture
def classes_code_no_methods():
    """Fixture for code containing classes with no methods."""
    return """
class ClassA:
    pass

class ClassB:
    pass
"""

@pytest.fixture
def classes_code_with_methods():
    """Fixture for code containing classes with methods."""
    return """
class ClassA:
    def m1(self): pass
    def m2(self): pass

class ClassB:
    def m3(self): pass
    def m4(self): pass
    def m5(self): pass
"""

@pytest.fixture
def functions_code_no_params():
    """Fixture for code containing a function with no parameters."""
    return """
def func1(): pass
"""

@pytest.fixture
def functions_code_with_params():
    """Fixture for code containing functions with parameters."""
    return """
def func1(a, b): pass

def func2(c, d, e, f): pass
"""

class TestAverageBasedMetrics:
    """
    Tests for average-based metrics
    """
    def test_average_lines_per_file_no_files(self, metrics, empty_file_list):
        """
        Test that the average number of lines per file is 0 when no files are provided.
        """
        result = metrics.\
            count_average_number_of_lines_per_file\
                (empty_file_list)
        assert result == 0

    def test_average_lines_per_file(self, metrics, multiple_files):
        """
        Test the calculation of the average number of lines per file with multiple files.
        """
        result = metrics\
            .count_average_number_of_lines_per_file\
                (multiple_files)
        assert result == (3 + 5) / 2

    def test_average_lines_per_method_no_methods(self, metrics):
        """
        Test that the average number of lines per method is 0 when no methods are provided.
        """
        result = metrics\
            .count_average_number_of_lines_per_method([])
        assert result == 0

    def test_average_lines_per_method(self, metrics, methods_code):
        """
        Test the calculation of the average number of lines per method.
        """
        tree = ast.parse(methods_code)
        parsed_files = [tree]

        result = metrics\
            .count_average_number_of_lines_per_method(parsed_files)
        assert result == (4 + 2) / 2

    def test_average_methods_per_class_no_classes(self, metrics):
        """
        Test that the average number of methods per class is 0 when no classes are provided.
        """
        result = metrics.\
            count_average_number_of_methods_per_class([])
        assert result == 0

    def test_average_methods_per_class_no_methods(self, metrics, classes_code_no_methods):
        """
        Test the calculation of the average number of methods per class - no methods.
        """
        tree = ast.parse(classes_code_no_methods)
        parsed_files = [tree]

        result = metrics.\
            count_average_number_of_methods_per_class(parsed_files)
        assert result == 0

    def test_average_methods_per_class(self, metrics, classes_code_with_methods):
        """
        Test the calculation of the average number of methods per class.
        """
        tree = ast.parse(classes_code_with_methods)
        parsed_files = [tree]

        result = metrics\
            .count_average_number_of_methods_per_class(parsed_files)
        assert result == (2 + 3) / 2

    def test_average_params_no_functions(self, metrics):
        """
        Test that the average number of parameters 
        per function/method is 0 when no functions are provided.
        """
        result = metrics\
            .count_average_number_of_params_per_method_or_function([])
        assert result == 0

    def test_average_params_per_method_no_params(self, metrics, functions_code_no_params):
        """
        Test the calculation of the average number of 
        parameters per function/method - no params.
        """
        tree = ast.parse(functions_code_no_params)
        parsed_files = [tree]

        result = metrics\
        .count_average_number_of_params_per_method_or_function(parsed_files)
        assert result == 0

    def test_average_params_per_method(self, metrics, functions_code_with_params):
        """
        Test the calculation of the average number of parameters per function/method.
        """
        tree = ast.parse(functions_code_with_params)
        parsed_files = [tree]

        result = metrics\
        .count_average_number_of_params_per_method_or_function(parsed_files)
        assert result == (2 + 4) / 2
