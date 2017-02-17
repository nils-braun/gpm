import os


def get_gpm_dir(base_dir):
    return os.path.join(base_dir, ".gpm")


def get_state_file(base_dir):
    return os.path.join(get_gpm_dir(base_dir), "state.db")


def get_config_file(base_dir):
    return os.path.join(get_gpm_dir(base_dir), "config")