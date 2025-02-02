import click

from models.ext_python_stats import ExtPythonStats

# C:/Users/ASUS/PycharmProjects/Django/blogengine
@click.command()
@click.option('--path', '-p', required=True, help='Path to the repository.', default="C:/Users/ASUS/PycharmProjects/Django/blogengine")
@click.option('--xml_file_name', '-x', required=True, help='Name of the output XML file.', default="result_python_extended_stats.xml")
def main(path, xml_file_name):
    """
    Main function of the project. Using an inserted path to the repository and a resultant XML filename,
    calculates a set of metrics described in models/metrics.tex

    Args:
        path (str): Path to the repository to analyse.
        xml_file_name (str): Name for a resultant XML file .

    Returns:
        None.
    """
    stats = ExtPythonStats(path)
    stats.calculate_metrics_list()
    stats.get_xml_report(xml_file_name)


if __name__ == "__main__":
    main()
