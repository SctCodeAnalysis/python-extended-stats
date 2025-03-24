"""
This module provides class metrics tests
"""

import ast
import sys
from pathlib import Path

import pytest

from python_ext_stats.metrics.class_metrics import ClassMetrics

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))


@pytest.fixture
def classmetrics() -> ClassMetrics:
    """Fixture providing initialized ClassMetrics instance."""
    return ClassMetrics()

@pytest.fixture
def empty_class_module() -> ast.Module:
    """AST module with empty class definition."""
    code = """
class EmptyClass:
    pass
"""
    return ast.parse(code)

@pytest.fixture
def simple_class_module() -> ast.Module:
    """AST module with emsimplepty class definition."""
    code = """
class EmptyClass:
    _heart = A()
    head = 4
    main: str
    _test: int

    def __init__(self):
        pass
    def test(self):
        pass
        
def hello():
    pass
"""
    return ast.parse(code)


@pytest.fixture
def simple__two_class_module() -> ast.Module:
    """AST module with emsimplepty class definition."""
    code = """
class A:
    def test(self):
        pass
    def hell(self):
        pass
    def olo(self):
        pass
class Test(A):
    _duck = datetime.utcnow()
    high: Text = ABC()
    @staticmethod
    def method(cls):
        print("hello")
    def test(self):
        pass
    def olo(self):
        pass
"""
    return ast.parse(code)

@pytest.fixture
def sample_inheritance_class_module() -> ast.Module:
    """AST module with inheritance class definition."""
    code = """
class One():
    pass
    
class EmptyClass(One):
    pass
    
class EmptyClassTwo:
    pass
    
class Alpha(EmptyClass, EmptyClassTwo):
    pass
    
class Beta(Alpha):
    pass
"""
    return ast.parse(code)


class TestClassMetrics:
    """Tests suite for ClassMetrics functionality."""

    def test_method_hiding_factor_empty_class(self, classmetrics: ClassMetrics,\
                                               empty_class_module: ast.Module):
        """
        Test CBO calculation for class without dependencies.
        Expected MHF: 0
        """
        result = classmetrics.calculate_method_hiding_factor([empty_class_module])
        assert result == 0

    def test_method_hiding_factor_simple_class(self, classmetrics: ClassMetrics,\
                                                simple_class_module: ast.Module):
        """
        Test CBO calculation for class without dependencies.
        Expected MHF: 0.5
        """
        result = classmetrics.calculate_method_hiding_factor([simple_class_module])
        assert result == 0.5

    def test_attribute_hiding_factor_empty_class(self, classmetrics: ClassMetrics,\
                                                  empty_class_module: ast.Module):
        """
        Test CBO calculation for class without dependencies.
        Expected MHF: 0
        """
        result = classmetrics.calculate_attribute_hiding_factor([empty_class_module])
        assert result == 0

    def test_attribute_hiding_factor_simple_class(self, classmetrics: ClassMetrics,\
                                                   simple_class_module: ast.Module):
        """
        Test CBO calculation for class without dependencies.
        Expected MHF: 0.5
        """
        result = classmetrics.\
            calculate_attribute_hiding_factor([simple_class_module])
        assert result == 0.5

    def test_method_inheritance_factor_empty_class(self, classmetrics: ClassMetrics,\
                                                    empty_class_module: ast.Module):
        """
        Test MIF calculation for class without dependencies.
        Expected MIF: 0
        """
        result = classmetrics.\
            calculate_method_inheritance_factor([empty_class_module])
        assert result["EmptyClass"] == 0

    def test_method_inheritance_factor_simple_class(self, classmetrics: ClassMetrics,\
                                                     simple__two_class_module: ast.Module):
        """
        Test MIF calculation for class with 1 dependency.
        Expected MIF: 0, 0.75
        """
        result = classmetrics.\
            calculate_method_inheritance_factor([simple__two_class_module])
        assert result["Test"] == 0.75 and result["A"] == 0.0

    def test_method_polymorphism_factor_empty_class(self, classmetrics: ClassMetrics,\
                                                     empty_class_module: ast.Module):
        """
        Test MPF calculation for class without dependencies.
        Expected MIF: 0
        """
        result = classmetrics.\
            calculate_method_polymorphism_factor([empty_class_module])
        assert result["EmptyClass"] == 0

    def test_method_polymorphism_factor_simple_class(self, classmetrics: ClassMetrics,\
                                                      simple__two_class_module: ast.Module):
        """
        Test MPF calculation for class with 1 dependency.
        Expected MIF: 0.5, 0
        """
        result = classmetrics.\
            calculate_method_polymorphism_factor([simple__two_class_module])
        assert result["Test"] == 0.5 and result["A"] == 0.0

    def test_depth_of_inheritance_tree_empty_class(self, classmetrics: ClassMetrics,\
                                                    empty_class_module: ast.Module):
        """
        Test MPF calculation for class without dependencies.
        Expected DIT: 1
        """
        result = classmetrics.\
            calculate_depth_of_inheritance_tree([empty_class_module])
        assert result == 1

    def test_depth_of_inheritance_tree_basic_classes(self, classmetrics: ClassMetrics,\
                                                      sample_inheritance_class_module: ast.Module):
        """
        Test MPF calculation for class with 1 dependency.
        Expected DIT: 4
        """
        result = classmetrics.\
            calculate_depth_of_inheritance_tree([sample_inheritance_class_module])
        assert result == 4
