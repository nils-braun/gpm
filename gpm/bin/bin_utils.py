from __future__ import print_function

import os

from gpm.utils.utils import get_gpm_dir


def find_next_gpm_base_dir(start_folder):
    start_folder = os.path.abspath(start_folder)

    if os.path.isdir(get_gpm_dir(start_folder)):
        return start_folder

    else:
        parent_dir = os.path.abspath(os.path.join(start_folder, os.path.pardir))
        if parent_dir == start_folder:
            return None

        return find_next_gpm_base_dir(parent_dir)


def assert_project(project):
    if project is None:
        raise RuntimeError("Could not find a gpm base path (not in the parent folders).")


def get_short_hash(commit_hash):
    return commit_hash[:6]


def format_commit(commit, show_file_content, show_externals):
    print("{hash}\tdate:\t\t{date}".format(hash=get_short_hash(commit._file_content_hash), date="1234"))
    print("\tcommit:\t\t{hash}".format(hash=commit._file_content_hash))
    print("\texternals:\t{hash}".format(hash=commit._state_hash))

    print("\n\tfile content:", end="")

    if show_file_content:
        print("File content where at this state")
        print(commit.file_content)
    else:
        print("File was {length} characters long".format(length=len(commit.file_content)))

    print("Externals where at this state {hash}".format(hash=commit._state_hash))
    if show_externals:
        print(commit.state)