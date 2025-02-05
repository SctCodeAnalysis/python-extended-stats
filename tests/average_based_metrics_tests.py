import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

import pytest
import ast
from typing import List

from models.average_based_metrics import AverageBasedMetrics

@pytest.fixture
def metrics():
    """
    Fixture to initialize an instance of AverageBasedMetrics.
    """
    return AverageBasedMetrics()

def test_average_lines_per_file_no_files(metrics):
    """
    Test that the average number of lines per file is 0 when no files are provided.
    """
    result = metrics._AverageBasedMetrics__count_average_number_of_lines_per_file([])
    assert result == 0

def test_average_lines_per_file(metrics, tmp_path):
    """
    Test the calculation of the average number of lines per file with multiple files.
    """
    file1 = tmp_path / "file1.py"
    file1.write_text("a = 1\nb = 2\nc = 3")
    
    file2 = tmp_path / "file2.py"
    file2.write_text("x = 4\ny = 5\nz = 6\nw = 7\nv = 8")
    
    files = [file1, file2]
    result = metrics._AverageBasedMetrics__count_average_number_of_lines_per_file(files)
    assert result == (3 + 5) / 2

def test_average_lines_per_method_no_methods(metrics):
    """
    Test that the average number of lines per method is 0 when no methods are provided.
    """
    result = metrics._AverageBasedMetrics__count_average_number_of_lines_per_method([])
    assert result == 0

def test_average_lines_per_method(metrics):
    """
    Test the calculation of the average number of lines per method.
    """
    code = """
def method1():
    a = 1
    b = 2
    c = 3

def method2():
    x = 4
"""
    tree = ast.parse(code)
    parsed_files = [tree]
    
    result = metrics._AverageBasedMetrics__count_average_number_of_lines_per_method(parsed_files)
    assert result == (4 + 2) / 2

def test_average_methods_per_class_no_classes(metrics):
    """
    Test that the average number of methods per class is 0 when no classes are provided.
    """
    result = metrics._AverageBasedMetrics__count_average_number_of_methods_per_class([])
    assert result == 0

def test_average_methods_per_class_no_methods(metrics):
    """
    Test the calculation of the average number of methods per class - no methods
    """
    code = """
class ClassA:
    pass

class ClassB:
    pass
"""
    tree = ast.parse(code)
    parsed_files = [tree]
    
    result = metrics._AverageBasedMetrics__count_average_number_of_methods_per_class(parsed_files)
    assert result == 0

def test_average_methods_per_class(metrics):
    """
    Test the calculation of the average number of methods per class.
    """
    code = """
class ClassA:
    def m1(self): pass
    def m2(self): pass

class ClassB:
    def m3(self): pass
    def m4(self): pass
    def m5(self): pass
"""
    tree = ast.parse(code)
    parsed_files = [tree]
    
    result = metrics._AverageBasedMetrics__count_average_number_of_methods_per_class(parsed_files)
    assert result == (2 + 3) / 2

def test_average_params_no_functions(metrics):
    """
    Test that the average number of parameters per function/method is 0 when no functions are provided.
    """
    result = metrics._AverageBasedMetrics__count_average_number_of_params_per_method_of_function([])
    assert result == 0

def test_average_params_per_method_no_params(metrics):
    """
    Test the calculation of the average number of parameters per function/method. - no params
    """
    code = """
def func1(): pass
"""
    tree = ast.parse(code)
    parsed_files = [tree]
    
    result = metrics._AverageBasedMetrics__count_average_number_of_params_per_method_of_function(parsed_files)
    assert result == 0

def test_average_params_per_method(metrics):
    """
    Test the calculation of the average number of parameters per function/method.
    """
    code = """
def func1(a, b): pass

def func2(c, d, e, f): pass
"""
    tree = ast.parse(code)
    parsed_files = [tree]
    
    result = metrics._AverageBasedMetrics__count_average_number_of_params_per_method_of_function(parsed_files)
    assert result == (2 + 4) / 2
