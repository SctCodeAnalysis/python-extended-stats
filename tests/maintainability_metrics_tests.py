"""
This module provides maintainability metrics tests
"""

import ast
import pytest

from python_ext_stats.metrics.maintainability_metrics import MaintainabilityMetrics


def parse_code_to_ast(code: str) -> ast.Module:
    """
    parses code to ast-tree
    """
    return ast.parse(code)

@pytest.fixture
def empty_file_ast() -> ast.Module:
    """
    returns empty ast-tree
    """
    return parse_code_to_ast("")

@pytest.fixture
def function_with_docstring_ast() -> ast.Module:
    """
    Test fixture for doctring
    """
    code = """
def my_function():
    '''This is a docstring'''
    pass
    """
    return parse_code_to_ast(code)

@pytest.fixture
def function_without_docstring_ast() -> ast.Module:
    """
    Test fixture for doctring-2
    """
    code = """
def my_function():
    pass
    """
    return parse_code_to_ast(code)

@pytest.fixture
def function_with_typing_ast() -> ast.Module:
    """
    Test fixture for typing
    """
    code = """
def my_function(a: int, b: str) -> float:
    return 1.0
    """
    return parse_code_to_ast(code)

@pytest.fixture
def function_without_typing_ast() -> ast.Module:
    """
    Test fixture for typing
    """
    code = """
def my_function(a, b):
    return 1
    """
    return parse_code_to_ast(code)

@pytest.fixture
def context_manager_ast() -> ast.Module:
    """
    Test fixture for context manager
    """
    code = """
with open('file.txt', 'r') as f:
    data = f.read()

with open("") as f:
    pass
    """
    return parse_code_to_ast(code)

@pytest.fixture
def try_except_ast() -> ast.Module:
    """
    Test fixture for try-except
    """
    code = """
try:
    result = 1 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
    """
    return parse_code_to_ast(code)

@pytest.fixture
def deprecated_function_ast() -> ast.Module:
    """
    Test fixture for deprecated function
    """
    code = """
@deprecated
def old_function():
    pass
"""
    return parse_code_to_ast(code)

@pytest.fixture
def deprecated_method_ast() -> ast.Module:
    """
    Test fixture for deprecated method - 2
    """
    code = """
class MyClass:
    @deprecated
    def old_method(self):
        pass
    """
    return parse_code_to_ast(code)

class TestMaintainabilityMetrics:
    """
    Tests for maintainability metrics
    """
    @pytest.fixture
    def maintainability_metrics(self):
        """
        Target class initializator
        """
        return MaintainabilityMetrics()

    def test_count_number_of_functions_or_methods_without_docstrings_empty(\
            self, maintainability_metrics, empty_file_ast):
        """
        test for counting number of funcs and methods without docsting in an empty file
        """
        assert maintainability_metrics.\
    count_number_of_functions_or_methods_without_docstrings\
        ([empty_file_ast]) == 0

    def test_count_number_of_functions_or_methods_without_docstrings_present(self,\
                            maintainability_metrics,\
                                  function_with_docstring_ast, function_without_docstring_ast):
        """
        test for counting number of funcs and methods without docstring in a basic file
        """
        asts = [function_with_docstring_ast, function_without_docstring_ast]
        assert maintainability_metrics.\
    count_number_of_functions_or_methods_without_docstrings\
            (asts) == 1

    def test_count_number_of_functions_or_methods_without_typing_empty(self,\
                                                    maintainability_metrics, empty_file_ast):
        """
        test for counting number of funcs and methods without typing in an empty file
        """
        assert maintainability_metrics.\
    count_number_of_functions_or_methods_without_typing\
        ([empty_file_ast]) == 0

    def test_count_number_of_functions_or_methods_without_typing_present(self, \
            maintainability_metrics, function_with_typing_ast, function_without_typing_ast):
        """
        test for counting number of funcs and methods without typing in a basic file
        """
        asts = [function_with_typing_ast, function_without_typing_ast]
        assert maintainability_metrics.\
        count_number_of_functions_or_methods_without_typing\
            (asts) == 1

    def test_count_number_of_context_managers_empty(self, maintainability_metrics, empty_file_ast):
        """
        test for counting a number of context managers in an empty file
        """
        assert maintainability_metrics.\
        count_number_of_context_managers([empty_file_ast]) == 0

    def test_count_number_of_context_managers_present(self, \
                                                    maintainability_metrics, context_manager_ast):
        """
        test for counting a number of context managers in an basic file
        """
        assert maintainability_metrics.\
        count_number_of_context_managers([context_manager_ast]) == 2

    def test_count_number_of_handled_exceptions_empty(self,\
                                                maintainability_metrics, empty_file_ast):
        """
        test for counting a number of handled exceptions in an empty file
        """
        assert maintainability_metrics.\
        count_number_of_handled_exceptions([empty_file_ast]) == 0

    def test_count_number_of_handled_exceptions_present(self,\
                                                 maintainability_metrics, try_except_ast):
        """
        test for counting a number of handled exceptions in a present file
        """
        assert maintainability_metrics.\
        count_number_of_handled_exceptions([try_except_ast]) == 1
