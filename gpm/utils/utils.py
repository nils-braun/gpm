import os


def get_gpm_dir(base_dir):
    return os.path.join(base_dir, ".gpm")


def get_state_file(base_dir):
    return os.path.join(get_gpm_dir(base_dir), "state.db")


def get_results_file(base_dir):
    return os.path.join(get_gpm_dir(base_dir), "results.db")


def get_config_file(base_dir):
    return os.path.join(get_gpm_dir(base_dir), "config")


def find_next_gpm_base_dir(start_folder="."):
    start_folder = os.path.abspath(start_folder)

    if os.path.isdir(get_gpm_dir(start_folder)):
        return start_folder

    else:
        parent_dir = os.path.abspath(os.path.join(start_folder, os.path.pardir))
        if parent_dir == start_folder:
            raise RuntimeError("Could not find a gpm base path (not in the parent folders).")

        return find_next_gpm_base_dir(parent_dir)