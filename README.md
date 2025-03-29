# Extended Statistics for Python repository

Taking source code repository as an input calculate extended statistics for Python source files.  

Base statistics include:
- Cyclomatic Complexity
- Halstead Complexity
- LCOM (Lack of Cohesion in Methods)
- Dead code
- Duplication Percentage
- Maximum Line Length
- Lines of Code (LOC)
- Average Line Length
- Average Identifier Length
- Number of pass keywords
- Method Hiding Factor
- Attribute Hiding Factor
- Method Inheritance Factor
- Polymorphism Factor
- Depth Of Inheritance Tree
- Response for a Class
- Code Maintainability
- Number of Methods Without Deprecation
- Number of Functions or Methods Without Docstrings
- Number of Functions or Methods Without Typing
- Number of Context Managers
- Number of Handled Exceptions
- Volatility Metric
- Clone Coverage
- Number of Classe
- Number of Methods
- Number of Static Methods
- Maximum Number of Method Parameters
- Maximum Method Length
- Number of Decorators
- Number of Public Constants in File
- Number of Libraries
- Number of Extensions in the Project
- CBO (Coupling Between Objects)
- Number of Files in the Project
- Depth of the Project File System Tree
- Average Number of Lines per File
- Average Number of Lines per Method
- Average Number of Methods per Class
- Average Number of Parameters per Method or Function

The stats are exposed as an API as well as exported report (in XML format)

## API Usage

```python
import python_extended_stats as st

stats = st.ExtPythonStats("path/to/repo")
report = "result_python_extended_stats.xml"

# Print available metrics
print(stats.metrics_list())

# Get calculated metrics as a dict
metrics_report_list = stats.report()

# Print XML report
stats.print(report, metrics_report_list)
```

## CLI Usage

```shell
\> python3 python-extended-stats --report_path <path_to_xml.xml> --path <path/to/repo>
```
