import os

from gpm import gpm
from gpm.utils.utils import find_next_gpm_base_dir

from argparse import ArgumentParser

import sys


def format_commit(commit, show_file_content, show_externals):
    print("File state {hash}".format(hash=commit._file_content_hash))

    if show_file_content:
        print("File content where at this state")
        print(commit.file_content)
    else:
        print("File was {length} characters long".format(length=len(commit.file_content)))

    if show_externals:
        print("Externals where at this state:")
        print(commit.state)
    else:
        print("Externals where at this state {hash}".format(hash=commit._state_hash))


def main():
    parser = ArgumentParser()

    parser.add_argument("result_file")
    parser.add_argument("--show-file-content", dest="show_file_content", action="store_true", default=False)
    parser.add_argument("--show-externals", dest="show_externals", action="store_true", default=False)

    args = parser.parse_args()

    result_file = os.path.abspath(args.result_file)

    project = gpm(find_next_gpm_base_dir("."))

    commits = project.get_results_for_file(result_file)

    print("Examining file {file_name}".format(file_name=args.result_file))
    print("")

    for commit in commits:
        print("----")
        format_commit(commit,
                      show_file_content=args.show_file_content,
                      show_externals=args.show_externals)

if __name__ == '__main__':
    sys.exit(main())