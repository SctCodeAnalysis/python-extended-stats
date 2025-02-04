import pytest
import ast
import sys
from pathlib import Path

from models.code_structure_metrics import CodeStructuresMetrics

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

@pytest.fixture
def metrics():
    """
    Fixture to initialize CodeStructuresMetrics instance.
    """
    return CodeStructuresMetrics()

def parse_code(code: str) -> ast.Module:
    """
    Parses a given Python code string into an AST module.
    
    :param code: The Python code as a string.
    :return: Parsed AST module.
    """
    return ast.parse(code)

class TestCodeStructureMetrics:
    """
    Test suite for CodeStructuresMetrics methods.
    """
    def test_count_classes_empty(self, metrics):
        """
        Test that an empty code string contains zero classes.
        """
        code = ""
        tree = parse_code(code)
        assert metrics._CodeStructuresMetrics__count_number_of_classes([tree]) == 0

    def test_count_classes_multiple(self, metrics):
        """
        Test that multiple class definitions are counted correctly.
        """
        code = """
class A: pass
class B: pass
"""
        tree = parse_code(code)
        assert metrics._CodeStructuresMetrics__count_number_of_classes([tree]) == 2

    def test_count_methods_empty(self, metrics):
        """
        Test that a function outside of a class is not counted as a class method.
        """
        code = "def func(): pass"
        tree = parse_code(code)
        assert metrics._CodeStructuresMetrics__count_number_of_methods_in_classes([tree]) == 0

    def test_count_methods_in_classes(self, metrics):
        """
        Test counting methods inside multiple classes.
        """
        code = """
class A:
    def m1(): pass
    def m2(): pass

class B:
    def m3(): pass
"""
        tree = parse_code(code)
        assert metrics._CodeStructuresMetrics__count_number_of_methods_in_classes([tree]) == 3

    def test_count_static_methods_empty(self, metrics):
        """
        Test that functions outside of a class are not counted as static methods.
        """
        code = "def func(): pass"
        tree = parse_code(code)
        assert metrics._CodeStructuresMetrics__count_number_of_static_methods_in_classes([tree]) == 0

    def test_count_static_methods(self, metrics):
        """
        Test counting static and class methods inside a class.
        """
        code = """
class A:
    @staticmethod
    def m1(): pass
    
    @classmethod
    def m2(cls): pass

@staticmethod
def func(): pass
"""
        tree = parse_code(code)
        assert metrics._CodeStructuresMetrics__count_number_of_static_methods_in_classes([tree]) == 2

    def test_max_params_empty(self, metrics):
        """
        Test that an empty code string has zero method parameters.
        """
        code = ""
        tree = parse_code(code)
        assert metrics._CodeStructuresMetrics__count_max_number_of_method_params([tree]) == 0

    def test_max_params(self, metrics):
        """
        Test finding the maximum number of parameters in functions and methods.
        """
        code = """
def func1(a, b): pass
def func2(c, d, e, f): pass
class A:
    def method(self, x, y, z): pass
"""
        tree = parse_code(code)
        assert metrics._CodeStructuresMetrics__count_max_number_of_method_params([tree]) == 4

    def test_max_method_length_empty(self, metrics):
        """
        Test that a single-line function has a maximum method length of 1.
        """
        code = "def func(): pass"
        tree = parse_code(code)
        assert metrics._CodeStructuresMetrics__count_max_method_length([tree]) == 1

    def test_max_method_length(self, metrics):
        """
        Test finding the maximum length of a method by counting lines.
        """
        code = """
def long_method():
    a = 1
    b = 2
    c = 3
    return a + b + c

def short(): pass
"""
        tree = parse_code(code)
        assert metrics._CodeStructuresMetrics__count_max_method_length([tree]) == 4

    def test_count_decorators_empty(self, metrics):
        """
        Test that functions without decorators are counted as having zero decorators.
        """
        code = "def func(): pass"
        tree = parse_code(code)
        assert metrics._CodeStructuresMetrics__count_number_of_decorators([tree]) == 0

    def test_count_decorators(self, metrics):
        """
        Test counting decorators in both class and function definitions.
        """
        code = """
@deco1
@deco2(arg)
class A:
    @deco3
    def method(self): pass

@deco4
def func(): pass
"""
        tree = parse_code(code)
        assert metrics._CodeStructuresMetrics__count_number_of_decorators([tree]) == 4

    def test_count_constants_empty(self, metrics):
        """
        Test that variables without uppercase names are not counted as constants.
        """
        code = "a = variable"
        tree = parse_code(code)
        assert metrics._CodeStructuresMetrics__count_number_of_constants([tree]) == 0

    def test_count_constants(self, metrics):
        """
        Test counting constants (uppercase variable assignments) in the code.
        """
        code = """
CONST = 100
NAME = 'test'
result = some_var
TEMP = 42.5
"""
        tree = parse_code(code)
        assert metrics._CodeStructuresMetrics__count_number_of_constants([tree]) == 3
