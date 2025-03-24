"""
This module provides CBO metric tests
"""

import sys
from pathlib import Path
import ast
import pytest

from python_ext_stats.metrics.CBO_metric import CBOMetric


PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))


@pytest.fixture
def cbometric() -> CBOMetric:
    """Fixture providing initialized CBOMetric instance."""
    return CBOMetric()

@pytest.fixture
def empty_class_module() -> ast.Module:
    """AST module with empty class definition."""
    code = """
class EmptyClass:
    pass
"""
    return ast.parse(code)

@pytest.fixture
def inheritance_class_module() -> ast.Module:
    """AST module with class inheritance."""
    code = """
class BaseClass:
    pass
    
class DerivedClass(BaseClass):
    pass
    """
    return ast.parse(code)

@pytest.fixture
def method_calls_module() -> ast.Module:
    """AST module with method calls to other classes."""
    code = """
class ClassA:
    def method_a(self):
        pass

class ClassB:
    def __init__(self):
        self.a = ClassA()
        
    def method_b(self):
        self.a.method_a()
        int_var = int(42)
"""
    return ast.parse(code)

@pytest.fixture
def complex_case_module() -> ast.Module:
    """AST module with combined inheritance and method calls."""
    code = """
class Parent:
    pass

class Child(Parent):
    def __init__(self):
        self.obj = OtherClass()
        
    def process(self):
        self.obj.execute()
        result = list()
"""
    return ast.parse(code)

class TestCBOMetric:
    """Test suite for CBOMetric functionality."""

    def test_empty_class_cbo(self, cbometric: CBOMetric, empty_class_module: ast.Module):
        """
        Test CBO calculation for class without dependencies.
        Expected CBO: 0
        """
        result = cbometric.count_coupling_between_objects([empty_class_module])
        assert result["EmptyClass"] == 0

    def test_inheritance_cbo(self, cbometric: CBOMetric, inheritance_class_module: ast.Module):
        """
        Test CBO calculation with class inheritance.
        Expected CBO for DerivedClass: 1 (BaseClass)
        """
        result = cbometric.count_coupling_between_objects([inheritance_class_module])
        assert result["DerivedClass"] == 1

    def test_method_calls_cbo(self, cbometric: CBOMetric, method_calls_module: ast.Module):
        """
        Test CBO calculation with method calls and object creation.
        Expected CBO:
        - ClassA: 0
        - ClassB: 1 (ClassA)
        """
        result = cbometric.count_coupling_between_objects([method_calls_module])
        print(f"CALCULATED RESULT: {result}")
        assert result["ClassA"] == 0
        assert result["ClassB"] == 1

    def test_complex_case_cbo(self, cbometric: CBOMetric, complex_case_module: ast.Module):
        """
        Test CBO calculation with combined inheritance and method calls.
        Expected CBO for Child: 2 (Parent + OtherClass)
        """
        result = cbometric.count_coupling_between_objects([complex_case_module])
        assert result["Child"] == 2
