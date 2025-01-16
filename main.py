import click

from models.ext_python_stat import ExtPythonStats


@click.command()
@click.option('--path', '-p', required=True, help='Path to the repository.')
@click.option('--xml_file_name', '-x', required=True, help='Name of the output XML file.')
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
    pass


if __name__ == "__main__":
    main()
