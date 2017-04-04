try:
    import cPickle as pickle
except ImportError:
    import pickle

import os


def get_db_file_path(folder):
    return os.path.join(folder, ".gpm/state.db")


class KeyValueDB:
    def __init__(self, db_folder):
        self.db_file_path = get_db_file_path(db_folder)
        self._dict = {}

    def _load(self):
        with open(self.db_file_path, "rb") as f:
            self._dict = pickle.load(f)

    def _save(self):
        if not os.path.exists(self.db_file_path):
            basename, filename = os.path.split(self.db_file_path)
            os.makedirs(basename)

        with open(self.db_file_path, "wb") as f:
            pickle.dump(self._dict, f)

    def __getitem__(self, item):
        self._load()
        return self._dict[item]

    def __setitem__(self, key, value):
        self._load()
        self._dict[key] = value
        self._save()