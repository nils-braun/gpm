import os

import simplejson


class KeyValueDatabase:
    def __init__(self, database_file):
        self.database_file = database_file
        self._database = {}

        if os.path.exists(database_file):
            self._load_db()

    def _load_db(self):
        with open(self.database_file, 'rb') as f:
            self._database = simplejson.load(f)

    def _store_db(self):
        with open(self.database_file, 'wb') as f:
            simplejson.dump(self._database, f)

    def set(self, key, value):
        self._database[key] = value
        self._store_db()

    def get(self, key):
        self._load_db()

        value = self._database[key]
        return value
