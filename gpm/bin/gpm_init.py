from gpm.utils.utils import get_gpm_dir

from argparse import ArgumentParser

import sys
import os


def main():
    parser = ArgumentParser()
    parser.add_argument("--base-path", default=".", dest="base_path")

    args = parser.parse_args()

    base_path = os.path.abspath(args.base_path)

    if not os.path.isdir(base_path):
        raise RuntimeError("Base path {base_path} is not present.".format(base_path=base_path))

    gpm_path = get_gpm_dir(base_path)

    if not os.path.isdir(gpm_path):
        os.mkdir(gpm_path)

if __name__ == '__main__':
    sys.exit(main())