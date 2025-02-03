import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

import unittest
import ast
import tempfile
from pathlib import Path
from typing import List, Dict

from models.average_based_metrics import AverageBasedMetrics

class TestAverageBasedMetrics(unittest.TestCase):
    def setUp(self):
        self.metrics = AverageBasedMetrics()
        self.py_files: List[Path] = []
        self.parsed_py_files: List[ast.Module] = []

    def tearDown(self):
        for file in self.py_files:
            file.unlink()

    def create_temp_py_file(self, content: str) -> Path:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
            tmp.write(content)
            tmp_path = Path(tmp.name)
            self.py_files.append(tmp_path)
            return tmp_path

    def parse_code(self, code: str) -> ast.Module:
        return ast.parse(code)

    def test_average_lines_per_file_no_files(self):
        result = self.metrics._AverageBasedMetrics__count_average_number_of_lines_per_file([])
        self.assertEqual(result, 0)

    def test_average_lines_per_file(self):
        self.create_temp_py_file("a = 1\nb = 2\nc = 3")
        self.create_temp_py_file("x = 4\ny = 5\nz = 6\nw = 7\nv = 8")
        
        result = self.metrics._AverageBasedMetrics__count_average_number_of_lines_per_file(self.py_files)
        self.assertEqual(result, (3 + 5) / 2)

    def test_average_lines_per_method_no_methods(self):
        result = self.metrics._AverageBasedMetrics__count_average_number_of_lines_per_method([])
        self.assertEqual(result, 0)

    def test_average_lines_per_method(self):
        code = """
def method1():
    a = 1
    b = 2
    c = 3

def method2():
    x = 4
"""
        tree = self.parse_code(code)
        self.parsed_py_files.append(tree)
        
        result = self.metrics._AverageBasedMetrics__count_average_number_of_lines_per_method(self.parsed_py_files)
        self.assertEqual(result, (4 + 2) / 2)

    def test_average_methods_per_class_no_classes(self):
        result = self.metrics._AverageBasedMetrics__count_average_number_of_methods_per_class([])
        self.assertEqual(result, 0)

    def test_average_methods_per_class(self):
        code = """
class ClassA:
    def m1(self): pass
    def m2(self): pass

class ClassB:
    def m3(self): pass
    def m4(self): pass
    def m5(self): pass
"""
        tree = self.parse_code(code)
        self.parsed_py_files.append(tree)
        
        result = self.metrics._AverageBasedMetrics__count_average_number_of_methods_per_class(self.parsed_py_files)
        self.assertEqual(result, (2 + 3) / 2)

    def test_average_params_no_functions(self):
        result = self.metrics._AverageBasedMetrics__count_average_number_of_params_per_method_of_function([])
        self.assertEqual(result, 0)

    def test_average_params_per_method(self):
        code = """
def func1(a, b): pass
def func2(c, d, e, f): pass
"""
        tree = self.parse_code(code)
        self.parsed_py_files.append(tree)
        
        result = self.metrics._AverageBasedMetrics__count_average_number_of_params_per_method_of_function(self.parsed_py_files)
        self.assertEqual(result, (2 + 4) / 2)

if __name__ == '__main__':
    unittest.main()