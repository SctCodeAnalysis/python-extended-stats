"""
This module provides project file structure metrics tests
"""

import sys
from pathlib import Path
import pytest

from python_ext_stats.metrics.project_file_structure_metrics import ProjectFileStructureMetrics


PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))


@pytest.fixture
def empty_parsed_files():
    """Fixture for an empty list of parsed files."""
    return []

@pytest.fixture
def one_level_repo_tree(tmp_path):
    """
    Sample tree
    """
    file1 = tmp_path / "script.py"
    file1.write_text("# Sample script")

    file2 = tmp_path / "data.csv"
    file2.write_text("col1,col2\nval1,val2")

    file3 = tmp_path / "report.txt"
    file3.write_text("This is a report.")

    all_files = list(tmp_path.rglob("*"))

    return all_files

@pytest.fixture
def three_level_repo_tree(tmp_path):
    """
    Sample 3-level tree 
    """
    file1 = tmp_path / "script.py"
    file1.write_text("# Sample script")

    file2 = tmp_path / "data.csv"
    file2.write_text("col1,col2\nval1,val2")

    file3 = tmp_path / "report.txt"
    file3.write_text("This is a report.")

    nested_dir = tmp_path / "two" / "three"
    nested_dir.mkdir(parents=True, exist_ok=True)
    file4 = nested_dir / "test.py"
    file4.write_text("print('Hello, world!')")

    all_files = [f for f in tmp_path.rglob("*") if f.is_file()]

    return all_files


class TestProjectFileStructureMetrics:
    """
    Tests for TestProjectFileStructureMetrics
    """
    @pytest.fixture
    def maintainability_metrics(self):
        """
        Provide ProjectFileStructureMetrics object
        """
        return ProjectFileStructureMetrics()

    def test_get_depth_of_the_project_file_system_tree_empty(self, empty_parsed_files,\
                                                              maintainability_metrics, tmp_path):
        """
        Tests for depth of an empty tree
        """
        assert maintainability_metrics.\
        get_depth_of_the_project_file_system_tree\
            (empty_parsed_files, Path(tmp_path)) == 0

    def test_get_depth_of_the_project_file_system_tree_basic(self, three_level_repo_tree,\
                                                              maintainability_metrics, tmp_path):
        """
        Tests for depth of an 3-level tree
        """
        assert maintainability_metrics.\
            get_depth_of_the_project_file_system_tree\
                (three_level_repo_tree, Path(tmp_path)) == 3
