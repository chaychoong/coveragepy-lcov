import click

from .converter import Converter


FILE_PATH = ".coverage"
RELATIVE_BOOL = True
CONFIG_FILE = True  # use True as default value


@click.command()
@click.option("--data_file_path", default=".coverage", help="Path to .coverage file")
@click.option(
    "--output_file_path", default="lcov.info", help="lcov.info output file path"
)
@click.option("--config_file", default=True, help="Path to .coveragerc file")
@click.option("--relative_path", is_flag=True, help="Use relative path in LCOV output")
@click.option("--preview", is_flag=True, help="Preview LCOV output")
def main(data_file_path, output_file_path, config_file, relative_path, preview):
    print(relative_path)
    converter = Converter(
        data_file_path=data_file_path,
        config_file=config_file,
        relative_path=relative_path,
    )
    if preview:
        converter.print_lcov()
    else:
        converter.create_lcov(output_file_path)
