# Extended Statistics for Python repository

Taking source code repository as an input calculate extended statistics for Python source files.  

Base statistics include:
- _(to be defined)_ 

The stats are exposed as an API as well as exported report (in XML format)

## API Usage

```python
import python_extended_stats as st

stats = ExtPythonStats("path/to/repo")

# Print available metrics
print(stats.list())

# Print number of classes
print(stats.metric("ADVANCED_METRIC"))

# Print XML report
print(stats.as_xml())
```

## CLI Usage

```shell
\> python3 python-extended-stats --report path_to_xml.xml path_to_repo
```
