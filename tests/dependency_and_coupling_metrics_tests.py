import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

import pytest
import ast
from models.project_metrics import ProjectMetrics
from models.dependency_and_coupling_metrics import DependencyAndCouplingMetrics


@pytest.fixture
def metrics():
    """
    Fixture to initialize an instance of DependencyAndCouplingMetrics.
    """
    return DependencyAndCouplingMetrics()

@pytest.fixture
def empty_parsed_files():
    """Fixture for an empty list of parsed files."""
    return []

@pytest.fixture
def parsed_files_with_imports():
    """Fixture for parsed files containing imports."""
    code = """
import os
import sys
import sys

from collections import defaultdict
from mymodule import MyClass
"""
    tree = ast.parse(code)
    return [tree]

@pytest.fixture
def all_files_with_extensions(tmp_path):
    """Fixture for a list of files with various extensions, excluding virtual environments."""
    file1 = tmp_path / "script.py"
    file1.write_text("# Sample script")
    
    file2 = tmp_path / "data.csv"
    file2.write_text("col1,col2\nval1,val2")
    
    file3 = tmp_path / "report.txt"
    file3.write_text("This is a report.")

    all_files = [
        f for f in tmp_path.rglob("*")
    ]
    
    return all_files

class TestDependencyAndCouplingMetrics:
    """
    Tests for dependency and coupling metrics
    """
    def test_count_number_of_libs_no_imports(self, metrics, empty_parsed_files):
        """
        Test that the number of libraries is zero when no imports are present.
        """
        result = metrics._DependencyAndCouplingMetrics__count_number_of_libs(empty_parsed_files)
        assert result == 0

    def test_count_number_of_libs_with_imports(self, metrics, parsed_files_with_imports):
        """
        Test counting unique libraries from parsed files with imports.
        """
        result = metrics._DependencyAndCouplingMetrics__count_number_of_libs(parsed_files_with_imports)
        assert result == 4  # os, sys, collections, mymodule

    def test_get_all_file_extensions_empty(self, metrics):
        """
        Test that no extensions are returned when no files are provided.
        """
        result = metrics._DependencyAndCouplingMetrics__get_all_file_extensions([])
        assert result == set()

    def test_get_all_file_extensions(self, metrics, all_files_with_extensions):
        """
        Test retrieving unique file extensions from a list of files, excluding virtual environments.
        """
        result = metrics._DependencyAndCouplingMetrics__get_all_file_extensions(all_files_with_extensions)
        
        # Ensure only valid extensions are included and the virtual environment file is ignored
        assert result == {'.py', '.csv', '.txt'}
