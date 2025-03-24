"""
This module provides code structures metrics tests
"""


import ast
import sys
from pathlib import Path
import pytest

from python_ext_stats.metrics.code_structure_metrics import CodeStructuresMetrics

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

@pytest.fixture
def metrics():
    """
    Fixture to initialize an instance of CodeStructuresMetrics.
    """
    return CodeStructuresMetrics()

def parse_code(code: str) -> ast.Module:
    """
    Parses a given Python code string into an AST module.
    
    :param code: The Python code as a string.
    :return: Parsed AST module.
    """
    return ast.parse(code)

@pytest.fixture
def empty_code():
    """Fixture for an empty code string."""
    return ""

@pytest.fixture
def multiple_classes_code():
    """Fixture for code with multiple class definitions."""
    return """
class A: pass
class B: pass
"""

@pytest.fixture
def function_code():
    """Fixture for a single function definition."""
    return "def func(): pass"

@pytest.fixture
def methods_in_classes_code():
    """Fixture for code with methods in multiple classes."""
    return """
class A:
    def m1(): pass
    def m2(): pass

class B:
    def m3(): pass
"""

@pytest.fixture
def static_methods_code():
    """Fixture for code with static and class methods."""
    return """
class A:
    @staticmethod
    def m1(): pass
    
    @staticmethod
    def m2(cls): pass

@staticmethod
def func(): pass
"""

@pytest.fixture
def max_params_code():
    """Fixture for code to test maximum number of parameters."""
    return """
def func1(a, b): pass
def func2(c, d, e, f): pass
class A:
    def method(self, x, y, z): pass
"""

@pytest.fixture
def max_method_length_code():
    """Fixture for code to test maximum method length."""
    return """
def long_method():
    a = 1
    b = 2
    c = 3
    return a + b + c

def short(): pass
"""

@pytest.fixture
def decorators_code():
    """Fixture for code containing decorators."""
    return """
@deco1
@deco2(arg)
class A:
    @deco3
    def method(self): pass

@deco4
def func(): pass
"""

@pytest.fixture
def constants_code():
    """Fixture for code containing constants."""
    return """
CONST = 100
NAME = 'test'
result = some_var
TEMP = 42.5
"""

class TestCodeStructureMetrics:
    """
    Test suite for CodeStructuresMetrics methods.
    """
    def test_count_classes_empty(self, metrics, empty_code):
        """Test that an empty code string contains zero classes."""
        tree = parse_code(empty_code)
        assert metrics.count_number_of_classes([tree]) == 0

    def test_count_classes_multiple(self, metrics, multiple_classes_code):
        """Test that multiple class definitions are counted correctly."""
        tree = parse_code(multiple_classes_code)
        assert metrics.count_number_of_classes([tree]) == 2

    def test_count_methods_empty(self, metrics, function_code):
        """Test that a function outside of a class is not counted as a class method."""
        tree = parse_code(function_code)
        assert metrics.count_number_of_methods_in_classes([tree]) == 0

    def test_count_methods_in_classes(self, metrics, methods_in_classes_code):
        """Test counting methods inside multiple classes."""
        tree = parse_code(methods_in_classes_code)
        assert metrics.count_number_of_methods_in_classes([tree]) == 3

    def test_count_static_methods_empty(self, metrics, function_code):
        """Test that functions outside of a class are not counted as static methods."""
        tree = parse_code(function_code)
        assert metrics.count_number_of_static_methods_in_classes\
            ([tree]) == 0

    def test_count_static_methods(self, metrics, static_methods_code):
        """Test counting static and class methods inside a class."""
        tree = parse_code(static_methods_code)
        assert metrics.count_number_of_static_methods_in_classes\
            ([tree]) == 3

    def test_max_params_empty(self, metrics, empty_code):
        """Test that an empty code string has zero method parameters."""
        tree = parse_code(empty_code)
        assert metrics.count_max_number_of_method_params([tree]) == 0

    def test_max_params_no_params(self, metrics):
        """Test that a method with no parameters returns zero."""
        code = """
class A:
    def method(): pass"""
        tree = parse_code(code)
        assert metrics.count_max_number_of_method_params([tree]) == 0

    def test_max_params(self, metrics, max_params_code):
        """Test finding the maximum number of parameters in functions and methods."""
        tree = parse_code(max_params_code)
        assert metrics.count_max_number_of_method_params([tree]) == 4

    def test_max_method_length_empty(self, metrics, function_code):
        """Test that a single-line function has a maximum method length of 1."""
        tree = parse_code(function_code)
        assert metrics.count_max_method_length([tree]) == 1

    def test_max_method_length(self, metrics, max_method_length_code):
        """Test finding the maximum length of a method by counting lines."""
        tree = parse_code(max_method_length_code)
        assert metrics.count_max_method_length([tree]) == 4

    def test_count_decorators_empty(self, metrics, function_code):
        """Test that functions without decorators are counted as having zero decorators."""
        tree = parse_code(function_code)
        assert metrics.count_number_of_decorators([tree]) == 0

    def test_count_decorators(self, metrics, decorators_code):
        """ 
        Test counting decorators in both class and function definitions. 
        """
        tree = parse_code(decorators_code)
        assert metrics.count_number_of_decorators([tree]) == 4

    def test_count_constants_empty(self, metrics, empty_code):
        """ 
        Test that variables without uppercase names are not counted as constants. 
        """
        tree = parse_code(empty_code)
        assert metrics.count_number_of_constants([tree]) == 0

    def test_count_constants(self, metrics, constants_code):
        """
        Test counting constants (uppercase variable assignments) in the code.
        """
        tree = parse_code(constants_code)
        assert metrics.count_number_of_constants([tree]) == 3
