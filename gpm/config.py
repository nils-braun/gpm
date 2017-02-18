import os

import configparser as configparser

from gpm.utils.utils import get_config_file, get_gpm_dir


class ConfigObject:
    def __init__(self, base_dir):
        self.base_dir = os.path.abspath(base_dir)

        self._assert_dir()
        self._read_config()

    def _read_config(self):
        config = configparser.ConfigParser()
        config.read(get_config_file(self.base_dir))

        self._externals = config.get("externals", "files", fallback="").splitlines()

    def _store_config(self):
        pass

    def _assert_dir(self):
        gpm_dir = get_gpm_dir(self.base_dir)
        if not os.path.isdir(gpm_dir):
            raise RuntimeError("Could not find a .gpm folder in folder '{base_dir}'. "
                               "Are you sure you have called 'gpm init'?".format(base_dir=self.base_dir))
