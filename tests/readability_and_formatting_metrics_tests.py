import pytest
import ast
from pathlib import Path
from models.readability_and_formatting_metrics import ReadabilityAndFormattingMetrics

class TestReadabilityAndFormattingMetrics:
    """Test suite for ReadabilityAndFormattingMetrics class."""

    @pytest.fixture
    def metrics(self):
        """Fixture providing initialized metrics calculator."""
        return ReadabilityAndFormattingMetrics()

    @pytest.fixture
    def duplicate_files(self, tmp_path):
        """Create two files with identical content."""
        file1 = tmp_path / "file1.py"
        file1.write_text("print('hello')\n")
        file2 = tmp_path / "file2.py"
        file2.write_text("print('hello')\n")
        return [file1, file2]

    @pytest.fixture
    def mixed_length_files(self, tmp_path):
        """Create files with varying line lengths."""
        file1 = tmp_path / "file1.py"
        file1.write_text(
"""a
bb
ccc""")
        file2 = tmp_path / "file2.py"
        file2.write_text("dddd")
        return [file1, file2]

    @pytest.fixture
    def multi_line_files(self, tmp_path):
        """Create files with different numbers of lines."""
        file1 = tmp_path / "file1.py"
        file1.write_text("\n\nprint('hello')\n# comment\n")
        file2 = tmp_path / "file2.py"
        file2.write_text("import sys\n")
        return [file1, file2]

    @pytest.fixture
    def parsed_identifiers(self):
        """Parse code with class/method/field identifiers."""
        code = """
class MyClass:
    def my_method(self):
        self.my_field = 1
    my_class_field = 2
"""
        return [ast.parse(code)]

    @pytest.fixture
    def parsed_empty_class(self):
        """Parse code with empty class definition."""
        code = "class EmptyClass: pass"
        return [ast.parse(code)]

    @pytest.fixture
    def parsed_pass_statements(self):
        """Parse code containing multiple pass keywords."""
        code = """
class MyClass:
    pass

def my_function():
    pass
"""
        return [ast.parse(code)]

    def test_duplication_percentage(self, metrics, duplicate_files):
        """Test duplicate line percentage calculation."""
        result = metrics._ReadabilityAndFormattingMetrics__calculate_duplication_percentage(duplicate_files)
        assert result == 50.0

    def test_max_line_length(self, metrics, mixed_length_files):
        """Test maximum line length detection."""
        max_length = metrics._ReadabilityAndFormattingMetrics__calculate_maximum_line_length(mixed_length_files)
        assert max_length == 4

    def test_lines_of_code_count(self, metrics, multi_line_files):
        """Test total lines of code counting."""
        loc = metrics._ReadabilityAndFormattingMetrics__count_lines_of_code(multi_line_files)
        assert loc == 5

    def test_average_line_length(self, metrics, mixed_length_files):
        """Test average line length calculation."""
        avg = metrics._ReadabilityAndFormattingMetrics__calculate_average_line_length(mixed_length_files)
        assert avg == 2.0 

    def test_identifier_lengths(self, metrics, parsed_identifiers):
        """Test average identifier length calculations."""
        result = metrics._ReadabilityAndFormattingMetrics__calculate_average_identifier_length(parsed_identifiers)
        assert result['class'] == 7.0
        assert result['method'] == 9.0
        assert result['field'] == 11.0

    def test_empty_class_identifiers(self, metrics, parsed_empty_class):
        """Test identifier lengths for empty class."""
        result = metrics._ReadabilityAndFormattingMetrics__calculate_average_identifier_length(parsed_empty_class)
        assert result['class'] == 10.0
        assert result['method'] == 0.0
        assert result['field'] == 0.0

    def test_pass_keyword_count(self, metrics, parsed_pass_statements):
        """Test pass keyword counting."""
        count = metrics._ReadabilityAndFormattingMetrics__count_number_pass_keywords(parsed_pass_statements)
        assert count == 2
