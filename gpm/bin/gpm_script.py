import os
import shutil

import click

from gpm import gpm
from gpm.bin.bin_utils import find_next_gpm_base_dir, assert_project, format_commit
from gpm.utils.utils import get_gpm_dir


@click.group()
@click.pass_context
def cli(ctx):
    next_gpm_base_dir = find_next_gpm_base_dir(".")
    if next_gpm_base_dir:
        project = gpm()
        ctx.obj = project


@cli.command()
@click.option('--overwrite/--no-overwrite', default=False)
@click.argument('base-path', default=".")
@click.pass_obj
def init(project, base_path, overwrite):
    """
    Initialize a new gpm.
    Either in the current folder (default), or in the given base path.
    """
    base_path = os.path.abspath(base_path)

    if not os.path.isdir(base_path):
        raise RuntimeError("Base path {base_path} is not present.".format(base_path=base_path))

    gpm_path = get_gpm_dir(base_path)

    if overwrite:
        shutil.rmtree(gpm_path)

    if not os.path.isdir(gpm_path):
        os.mkdir(gpm_path)


@cli.command()
@click.argument("result-file")
@click.option("--show-file-content/--no-show-file-content", default=False)
@click.option("--show-externals/--no-show-externals", default=False)
@click.pass_obj
def log(project, result_file, show_file_content, show_externals):
    """
    Show information on a given result file.
    e.g. which file contents where calculation with which external states.
    """
    assert_project(project)

    result_file = os.path.abspath(result_file)
    commits = project.get_results_for_file(result_file)

    print("Examining file {file_name}".format(file_name=result_file))
    print("")

    for commit in commits:
        format_commit(commit,
                      show_file_content=show_file_content,
                      show_externals=show_externals)

if __name__ == '__main__':
    cli()