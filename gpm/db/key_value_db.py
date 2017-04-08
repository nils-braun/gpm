from collections import defaultdict

try:
    import cPickle as pickle
except ImportError:
    import pickle

import os


def get_db_file_path(folder):
    if not folder:
        folder = os.getcwd()
    return os.path.join(folder, ".gpm/states/")


class KeyValueDB:
    def __init__(self, db_folder):
        self.db_file_path = get_db_file_path(db_folder)
        self._dict = defaultdict(dict)

    def _load(self, stub):
        db_file_path = self._get_filename(stub)
        if os.path.exists(db_file_path):
            with open(db_file_path, "rb") as f:
                self._dict[stub] = pickle.load(f)

    def _save(self, stub):
        db_file_path = self._get_filename(stub)

        if not os.path.exists(db_file_path):
            basename, filename = os.path.split(db_file_path)
            if basename and not os.path.exists(basename):
                os.makedirs(basename)

        with open(db_file_path, "wb") as f:
            pickle.dump(self._dict[stub], f)

    @staticmethod
    def _get_stub(key):
        return key[-2:]

    def _get_filename(self, stub):
        return os.path.join(self.db_file_path, stub + ".db")

    def __getitem__(self, item):
        stub = self._get_stub(item)

        self._load(stub)
        return self._dict[stub][item]

    def __setitem__(self, key, value):
        stub = self._get_stub(key)

        self._load(stub)
        self._dict[stub][key] = value
        self._save(stub)