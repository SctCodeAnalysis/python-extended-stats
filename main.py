"""
This module is the main script to activate the python-ext-stats
"""
import click

from python_ext_stats.ext_python_stats import ExtPythonStats


@click.command()
@click.option('--path', '-p', required=True, help='Path to the repository.')
@click.option('--report_file', '-r', required=True, help='Name of the report file.',
               default="result_python_extended_stats.xml")
def main(path="", report_file=""):
    """
    Main function of the project. Using an inserted path to the repository
    and a resultant XML filename,
    calculates a set of metrics described in models/metrics.tex

    Args:
        path (str): Path to the repository to analyse.
        xml_file_name (str): Name for a resultant XML file .

    Returns:
        None.
    """
    try:
        stats = ExtPythonStats(path)
        metrics_report_list = stats.report()
        stats.print(report_file, metrics_report_list)
    except Exception as e:
        print(f"Got an exception here: {e}")


if __name__ == "__main__":
    main()
